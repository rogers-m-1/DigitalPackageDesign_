"""Comparison logic service."""
from typing import Dict, List, Any
from app.schemas.comparison import PropertyDelta, ComparisonResultSchema


def calculate_property_deltas(
    uploaded_properties: Dict[str, float],
    reference_properties: Dict[str, float],
) -> List[PropertyDelta]:
    """
    Calculate property deltas between uploaded and reference designs.

    Args:
        uploaded_properties: Extracted properties from uploaded file
        reference_properties: Properties from reference library entry

    Returns:
        List of PropertyDelta objects with calculations
    """
    deltas = []

    # Standard property names
    property_names = [
        "length",
        "width",
        "height",
        "cap_length",
        "cap_width",
        "cap_height",
    ]

    for prop_name in property_names:
        uploaded_val = uploaded_properties.get(prop_name, 0.0)
        reference_val = reference_properties.get(prop_name, 0.0)
        delta = uploaded_val - reference_val

        deltas.append(
            PropertyDelta(
                property_name=prop_name,
                uploaded_value=uploaded_val,
                reference_value=reference_val,
                delta=delta,
                unit="mm",
            )
        )

    return deltas
