"""Export service for PDF and CSV generation."""
from typing import List, Dict, Any
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from datetime import datetime
import csv
from app.schemas.comparison import PropertyDelta
from app.utils.logging import get_logger

logger = get_logger(__name__)


def generate_pdf_export(
    uploaded_name: str,
    reference_name: str,
    properties: List[PropertyDelta],
) -> bytes:
    """
    Generate PDF report of comparison results.

    Args:
        uploaded_name: Name of uploaded design
        reference_name: Name of reference design
        properties: List of property deltas

    Returns:
        PDF file content as bytes
    """
    try:
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Build document content
        elements = []
        styles = getSampleStyleSheet()

        # Title
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1e3a8a"),
            spaceAfter=12,
        )
        elements.append(
            Paragraph(
                "Geometric Property Comparison Report",
                title_style,
            )
        )
        elements.append(Spacer(1, 0.2 * inch))

        # Metadata
        meta_data = [
            [
                "Uploaded Design:",
                uploaded_name,
            ],
            ["Reference Design:", reference_name],
            ["Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ]

        meta_table = Table(meta_data, colWidths=[2 * inch, 4 * inch])
        meta_table.setStyle(
            TableStyle(
                [
                    ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 10),
                    ("FONT", (1, 0), (1, -1), "Helvetica", 10),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
                ]
            )
        )
        elements.append(meta_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Results Table
        table_data = [
            [
                "Property",
                f"Uploaded\n({uploaded_name})",
                f"Reference\n({reference_name})",
                "Delta (Δ)",
            ]
        ]

        for prop in properties:
            table_data.append(
                [
                    prop.property_name,
                    f"{prop.uploaded_value:.2f} {prop.unit or ''}",
                    f"{prop.reference_value:.2f} {prop.unit or ''}",
                    f"{prop.delta:+.2f} {prop.unit or ''}",
                ]
            )

        results_table = Table(
            table_data,
            colWidths=[2 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch],
        )

        results_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
                ]
            )
        )

        elements.append(results_table)

        # Build PDF
        doc.build(elements)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()

    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        raise


def generate_csv_export(
    uploaded_name: str,
    reference_name: str,
    properties: List[PropertyDelta],
) -> bytes:
    """
    Generate CSV export of comparison results.

    Args:
        uploaded_name: Name of uploaded design
        reference_name: Name of reference design
        properties: List of property deltas

    Returns:
        CSV file content as bytes
    """
    try:
        csv_buffer = BytesIO()
        text_wrapper = io.StringIO()

        writer = csv.writer(text_wrapper)

        # Header metadata
        writer.writerow(["PRE Comparison Results"])
        writer.writerow(["Generated", datetime.now().isoformat()])
        writer.writerow([])

        # Comparison metadata
        writer.writerow(["Uploaded Design", uploaded_name])
        writer.writerow(["Reference Design", reference_name])
        writer.writerow([])

        # Results table headers
        writer.writerow(
            [
                "Property Name",
                f"Uploaded Value ({uploaded_name})",
                f"Reference Value ({reference_name})",
                "Delta (Δ)",
                "Unit",
            ]
        )

        # Results rows
        for prop in properties:
            writer.writerow(
                [
                    prop.property_name,
                    f"{prop.uploaded_value:.2f}",
                    f"{prop.reference_value:.2f}",
                    f"{prop.delta:+.2f}",
                    prop.unit or "",
                ]
            )

        # Convert StringIO to bytes
        csv_content = text_wrapper.getvalue().encode("utf-8")
        return csv_content

    except Exception as e:
        logger.error(f"CSV generation failed: {e}")
        raise


# Add missing import
import io
