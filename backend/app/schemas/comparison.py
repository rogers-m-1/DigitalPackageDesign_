"""Pydantic schemas for comparison operations."""
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime


class PropertyDelta(BaseModel):
    """Single property comparison result."""
    property_name: str
    uploaded_value: float
    reference_value: float
    delta: float
    unit: Optional[str] = None


class ComparisonResultSchema(BaseModel):
    """Full comparison results."""
    session_id: str
    uploaded_design_name: str
    reference_design_id: str
    reference_design_name: str
    properties: List[PropertyDelta]
    timestamp: datetime


class STPPropertiesSchema(BaseModel):
    """Extracted STP geometric properties."""
    length: float = Field(description="Overall length in mm")
    width: float = Field(description="Overall width in mm")
    height: float = Field(description="Overall height in mm")
    cap_length: float = Field(description="Bottle cap length in mm")
    cap_width: float = Field(description="Bottle cap width in mm")
    cap_height: float = Field(description="Bottle cap height in mm")
    additional_properties: Dict[str, float] = Field(default_factory=dict)


class UploadSTPSchema(BaseModel):
    """Request schema for STP file upload."""
    reference_design_id: Optional[str] = None
    reference_design_name: Optional[str] = None
