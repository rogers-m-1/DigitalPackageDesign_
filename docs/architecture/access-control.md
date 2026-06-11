# Access Control & Role-Based Permissions

## Role Definitions

### 1. **Viewer**
- **Who:** Design reviewers who only compare designs
- **Capabilities:**
  - Upload and compare .stp files against reference library
  - View own comparison history
  - Export comparison results (PDF, CSV)
  - View reference library (read-only)
  - Search and filter library designs
- **Restrictions:**
  - Cannot upload designs to library
  - Cannot modify or delete library entries
  - Cannot delete own comparisons (stored for audit)
  - Cannot see other users' comparisons

### 2. **Contributor**
- **Who:** Design engineers who populate and curate the reference library
- **Capabilities:**
  - All Viewer permissions
  - Upload .stp files to reference library
  - Bulk import designs via CSV
  - Edit metadata of own uploaded designs (rename, tags)
  - Delete own uploaded designs (but not others')
  - Upload multiple design variants
- **Restrictions:**
  - Cannot delete designs uploaded by others
  - Cannot edit user permissions
  - Cannot see audit logs

### 3. **Admin**
- **Who:** Library managers and platform owners
- **Capabilities:**
  - All Contributor permissions
  - Delete any design (including others' uploads)
  - Edit any design (rename, tags, metadata)
  - Manage user roles (promote/demote)
  - View full audit log
  - Access system settings and configuration
  - Bulk operations (tag management, archival)
- **Restrictions:**
  - Cannot modify user Azure AD profiles (read-only from Azure AD)

---

## Permission Matrix

| Action | Viewer | Contributor | Admin |
|--------|--------|-------------|-------|
| **Upload & Compare** | ✅ | ✅ | ✅ |
| **View own comparisons** | ✅ | ✅ | ✅ |
| **Export results** | ✅ | ✅ | ✅ |
| **Browse library** | ✅ | ✅ | ✅ |
| **Upload to library (STP)** | ❌ | ✅ | ✅ |
| **Import library (CSV)** | ❌ | ✅ | ✅ |
| **Edit own design metadata** | ❌ | ✅ | ✅ |
| **Delete own design** | ❌ | ✅ | ✅ |
| **Delete others' designs** | ❌ | ❌ | ✅ |
| **Manage user roles** | ❌ | ❌ | ✅ |
| **View audit logs** | ❌ | ❌ | ✅ |

---

## Implementation Details

### Azure AD Integration
- Users authenticate via Azure AD SSO
- Role stored in local database \users.role\ column (not in Azure AD)
- On first login: create user record with default role "viewer"
- Admin creates additional accounts and assigns roles via backend admin panel

### API Permission Checks
Every endpoint checks user role before processing:

\\\python
# Example FastAPI middleware
from fastapi import Depends, HTTPException

def require_role(required_roles: List[str]):
    async def check_role(current_user: User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return check_role

# Usage
@app.delete("/library/designs/{design_id}")
async def delete_design(design_id: str, user: User = Depends(require_role(["admin", "contributor"]))):
    # Check: is user the owner, or admin?
    design = db.query(DesignLibraryEntry).filter_by(id=design_id).first()
    if design.created_by_user_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Cannot delete another user's design")
    db.delete(design)
    return {"status": "deleted"}
\\\

### Frontend Permission Checks
- Show/hide UI elements based on role (e.g., hide "Delete" button for non-admins)
- Disable buttons with \disabled\ attribute if user lacks permission
- Use role store to guard route access (redirect to home if unauthorized)

---

## Default Roles & Onboarding

### First Admin Setup
1. During deployment, create first admin account manually
2. First admin uses admin panel to create additional accounts

### New User Workflow
1. User attempts login via Azure AD
2. System checks if user exists in \users\ table
3. If new: create record with default role "viewer"
4. Admin upgrades to "contributor" or "admin" as needed

---

## Audit Trail

All role-sensitive actions are logged in \udit_logs\:
- Design uploads, deletes, modifications
- User role changes
- Sensitive data exports

\\\sql
INSERT INTO audit_logs (user_id, action, resource_type, resource_id, details)
VALUES (?, 'delete_design', 'design_library_entry', ?, { \"design_name\": \"Bottle-v2.1\" });
\\\

---

## Security Considerations

- **Token expiry:** Azure AD tokens expire after 1 hour; refresh tokens handled by MSAL.js
- **CORS:** Backend restricts API calls to authorized frontend domain
- **Input validation:** All user inputs validated server-side (never trust client)
- **Rate limiting:** API endpoints rate-limited per user to prevent abuse
- **Encryption:** Passwords never stored; only Azure AD tokens + JWT

