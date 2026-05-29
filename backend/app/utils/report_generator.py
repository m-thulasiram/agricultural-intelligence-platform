import io
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie

REPORT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "reports",
)


class ReportBranding:
    COMPANY_NAME = "CropAI Health Forecasting"
    TAGLINE = "Intelligent Agricultural Intelligence Platform"
    PRIMARY_COLOR = colors.HexColor("#15803d")
    SECONDARY_COLOR = colors.HexColor("#166534")
    ACCENT_COLOR = colors.HexColor("#22c55e")
    BACKGROUND_COLOR = colors.HexColor("#f0fdf4")
    TEXT_COLOR = colors.HexColor("#1f2937")
    LIGHT_GRAY = colors.HexColor("#f3f4f6")
    DARK_GRAY = colors.HexColor("#6b7280")


def _ensure_report_dir():
    os.makedirs(REPORT_DIR, exist_ok=True)


def _create_header(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(ReportBranding.PRIMARY_COLOR)
    canvas.rect(0, doc.pagesize[1] - 60, doc.pagesize[0], 60, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(40, doc.pagesize[1] - 42, ReportBranding.COMPANY_NAME)
    canvas.setFont("Helvetica", 10)
    canvas.drawString(40, doc.pagesize[1] - 58, ReportBranding.TAGLINE)
    canvas.setFillColor(ReportBranding.DARK_GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        doc.pagesize[0] - 40, 15, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    canvas.drawRightString(
        doc.pagesize[0] - 40, 5, f"Page {doc.page}"
    )
    canvas.setStrokeColor(ReportBranding.PRIMARY_COLOR)
    canvas.setLineWidth(2)
    canvas.line(40, 58, doc.pagesize[0] - 40, 58)
    canvas.restoreState()


def _build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReportTitle", fontName="Helvetica-Bold", fontSize=24,
        textColor=ReportBranding.PRIMARY_COLOR, spaceAfter=6, alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="ReportSubtitle", fontName="Helvetica", fontSize=12,
        textColor=ReportBranding.DARK_GRAY, spaceAfter=20, alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="SectionTitle", fontName="Helvetica-Bold", fontSize=16,
        textColor=ReportBranding.SECONDARY_COLOR, spaceBefore=20, spaceAfter=10,
        borderPadding=(0, 0, 4, 0),
    ))
    styles.add(ParagraphStyle(
        name="SubSectionTitle", fontName="Helvetica-Bold", fontSize=12,
        textColor=ReportBranding.TEXT_COLOR, spaceBefore=12, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="BodyText2", fontName="Helvetica", fontSize=10,
        textColor=ReportBranding.TEXT_COLOR, spaceAfter=6, leading=14,
    ))
    styles.add(ParagraphStyle(
        name="TableCell", fontName="Helvetica", fontSize=9,
        textColor=ReportBranding.TEXT_COLOR, leading=12,
    ))
    styles.add(ParagraphStyle(
        name="TableHeader", fontName="Helvetica-Bold", fontSize=9,
        textColor=colors.white, leading=12, alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="Footer", fontName="Helvetica", fontSize=8,
        textColor=ReportBranding.DARK_GRAY, alignment=TA_CENTER,
    ))
    return styles


def _build_data_table(headers: List[str], rows: List[List[str]]) -> Table:
    styles = _build_styles()
    table_data = [
        [Paragraph(h, styles["TableHeader"]) for h in headers]
    ]
    for row in rows:
        table_data.append([Paragraph(str(cell), styles["TableCell"]) for cell in row])

    col_widths = [max(1.2 * inch, len(h) * 7) for h in headers]
    total_width = sum(col_widths)
    page_width = A4[0] - 80
    if total_width > page_width:
        col_widths = [w * (page_width / total_width) for w in col_widths]

    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ReportBranding.PRIMARY_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, ReportBranding.LIGHT_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ReportBranding.BACKGROUND_COLOR]),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("TOPPADDING", (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
    ]))
    return table


def _build_metric_card(label: str, value: str, color: colors.Color = None) -> Table:
    if color is None:
        color = ReportBranding.PRIMARY_COLOR
    card_data = [
        [Paragraph(label, ParagraphStyle(
            "card_label", fontName="Helvetica", fontSize=9, textColor=ReportBranding.DARK_GRAY,
            alignment=TA_CENTER, spaceAfter=2,
        ))],
        [Paragraph(value, ParagraphStyle(
            "card_value", fontName="Helvetica-Bold", fontSize=18, textColor=color,
            alignment=TA_CENTER,
        ))],
    ]
    card = Table(card_data, colWidths=[1.8 * inch])
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ReportBranding.BACKGROUND_COLOR),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 1, ReportBranding.PRIMARY_COLOR),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return card


def generate_forecast_report(forecast_data: Dict[str, Any]) -> str:
    _ensure_report_dir()
    styles = _build_styles()
    region = forecast_data.get("region", "Unknown Region")
    forecasts = forecast_data.get("forecasts", [])
    filename = f"forecast_report_{region}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(REPORT_DIR, filename)

    doc = SimpleDocTemplate(
        filepath, pagesize=A4,
        leftMargin=40, rightMargin=40, topMargin=80, bottomMargin=40,
    )
    story = []

    story.append(Paragraph("Crop Forecast Report", styles["ReportTitle"]))
    story.append(Paragraph(f"Region: {region}", styles["ReportSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=2, color=ReportBranding.PRIMARY_COLOR))
    story.append(Spacer(1, 12))

    summary_data = [
        ["Total Forecast Years", str(len(forecasts))],
        ["Start Year", str(forecasts[0]["year"]) if forecasts else "N/A"],
        ["End Year", str(forecasts[-1]["year"]) if forecasts else "N/A"],
        ["Report Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    ]
    if forecasts:
        avg_yield = sum(f.get("predicted_yield", 0) for f in forecasts) / len(forecasts)
        summary_data.append(["Average Predicted Yield", f"{avg_yield:.2f} t/ha"])

    story.append(Paragraph("Summary", styles["SectionTitle"]))
    story.append(_build_data_table(["Metric", "Value"], summary_data))
    story.append(Spacer(1, 12))

    if forecasts:
        story.append(Paragraph("Yearly Forecast Details", styles["SectionTitle"]))
        headers = ["Year", "Predicted Yield (t/ha)", "Rainfall (mm)", "Temperature (°C)", "Confidence"]
        rows = [
            [
                f["year"],
                f"{f.get('predicted_yield', 0):.2f}",
                f"{f.get('rainfall_predicted', 0):.1f}",
                f"{f.get('temperature_predicted', 0):.1f}",
                f"{f.get('confidence', 0) * 100:.0f}%",
            ]
            for f in forecasts
        ]
        story.append(_build_data_table(headers, rows))
        story.append(Spacer(1, 12))

        years = [str(f["year"]) for f in forecasts]
        yields = [f.get("predicted_yield", 0) for f in forecasts]

        drawing = Drawing(460, 200)
        bc = VerticalBarChart()
        bc.x = 60
        bc.y = 40
        bc.height = 140
        bc.width = 380
        bc.data = [yields]
        bc.categoryAxis.categoryNames = years
        bc.categoryAxis.labels.fontSize = 8
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max(yields) * 1.3 if yields else 10
        bc.valueAxis.valueStep = max(yields) * 0.15 if yields else 1
        bc.bars[0].fillColor = ReportBranding.PRIMARY_COLOR
        bc.bars[0].strokeColor = ReportBranding.SECONDARY_COLOR
        bc.categoryAxis.labels.angle = 45
        drawing.add(bc)
        story.append(Paragraph("Yield Forecast Chart", styles["SubSectionTitle"]))
        story.append(drawing)

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=ReportBranding.LIGHT_GRAY))
    story.append(Paragraph(
        f"This report was generated by {ReportBranding.COMPANY_NAME}. "
        "The forecasts are based on historical data and ML models. "
        "Actual results may vary due to unforeseen environmental factors.",
        styles["Footer"],
    ))

    doc.build(story, onFirstPage=_create_header, onLaterPages=_create_header)
    return filepath


def generate_prediction_report(prediction_data: Dict[str, Any]) -> str:
    _ensure_report_dir()
    styles = _build_styles()
    item = prediction_data.get("item", "Unknown Crop")
    year = prediction_data.get("year", datetime.now().year)
    predicted_yield = prediction_data.get("predicted_yield", 0)
    confidence = prediction_data.get("confidence")
    filename = f"prediction_report_{item}_{year}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(REPORT_DIR, filename)

    doc = SimpleDocTemplate(
        filepath, pagesize=A4,
        leftMargin=40, rightMargin=40, topMargin=80, bottomMargin=40,
    )
    story = []

    story.append(Paragraph("Crop Yield Prediction Report", styles["ReportTitle"]))
    story.append(Paragraph(f"{item} - {year}", styles["ReportSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=2, color=ReportBranding.PRIMARY_COLOR))
    story.append(Spacer(1, 12))

    metrics = [
        _build_metric_card("Predicted Yield", f"{predicted_yield:.2f} t/ha"),
    ]
    if confidence is not None:
        metrics.append(_build_metric_card("Confidence", f"{confidence * 100:.0f}%"))
    metrics.append(_build_metric_card("Crop", item))
    metrics.append(_build_metric_card("Year", str(year)))

    metrics_table = Table([metrics], colWidths=[1.8 * inch] * len(metrics))
    metrics_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 16))

    details = [
        ["Crop Item", item],
        ["Prediction Year", str(year)],
        ["Predicted Yield", f"{predicted_yield:.2f} tonnes per hectare"],
    ]
    if confidence is not None:
        details.append(["Confidence Score", f"{confidence:.2f} ({confidence * 100:.0f}%)"])
    details.append(["Report Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    story.append(Paragraph("Prediction Details", styles["SectionTitle"]))
    story.append(_build_data_table(["Field", "Value"], details))

    if "input_features" in prediction_data:
        story.append(Spacer(1, 12))
        story.append(Paragraph("Input Features", styles["SectionTitle"]))
        input_features = prediction_data["input_features"]
        headers = ["Feature", "Value"]
        rows = [[k, str(v)] for k, v in input_features.items()]
        story.append(_build_data_table(headers, rows))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=ReportBranding.LIGHT_GRAY))
    story.append(Paragraph(
        f"This prediction was generated by {ReportBranding.COMPANY_NAME} ML models. "
        "Results are for reference and planning purposes only.",
        styles["Footer"],
    ))

    doc.build(story, onFirstPage=_create_header, onLaterPages=_create_header)
    return filepath


def generate_full_report(report_data: Dict[str, Any]) -> str:
    _ensure_report_dir()
    styles = _build_styles()
    region = report_data.get("region", "Unknown Region")
    filename = f"comprehensive_report_{region}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(REPORT_DIR, filename)

    doc = SimpleDocTemplate(
        filepath, pagesize=A4,
        leftMargin=40, rightMargin=40, topMargin=80, bottomMargin=40,
    )
    story = []

    story.append(Paragraph("Comprehensive Crop Health Report", styles["ReportTitle"]))
    story.append(Paragraph(f"Region: {region}", styles["ReportSubtitle"]))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["ReportSubtitle"],
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=ReportBranding.PRIMARY_COLOR))
    story.append(Spacer(1, 12))

    if "predictions" in report_data and report_data["predictions"]:
        story.append(Paragraph("Yield Predictions", styles["SectionTitle"]))
        headers = ["Crop", "Year", "Predicted Yield (t/ha)", "Confidence"]
        rows = []
        for p in report_data["predictions"]:
            conf = p.get("confidence")
            rows.append([
                p.get("item", "N/A"),
                str(p.get("year", "N/A")),
                f"{p.get('predicted_yield', 0):.2f}",
                f"{conf * 100:.0f}%" if conf else "N/A",
            ])
        story.append(_build_data_table(headers, rows))
        story.append(Spacer(1, 12))

    if "forecasts" in report_data and report_data["forecasts"]:
        story.append(PageBreak())
        story.append(Paragraph("Climate Forecasts", styles["SectionTitle"]))
        headers = ["Year", "Rainfall (mm)", "Temperature (°C)", "Drought (%)", "Flood (%)", "Confidence"]
        rows = []
        for f in report_data["forecasts"]:
            rows.append([
                str(f.get("year", "N/A")),
                f"{f.get('rainfall_predicted', 0):.1f}",
                f"{f.get('temperature_predicted', 0):.1f}",
                f"{f.get('drought_probability', 0) * 100:.0f}%",
                f"{f.get('flood_probability', 0) * 100:.0f}%",
                f"{f.get('confidence', 0) * 100:.0f}%",
            ])
        story.append(_build_data_table(headers, rows))
        story.append(Spacer(1, 12))

    if "disease_risks" in report_data and report_data["disease_risks"]:
        story.append(Paragraph("Disease Risk Assessment", styles["SectionTitle"]))
        headers = ["Crop Type", "Pest Attack (%)", "Disease Outbreak (%)", "Seasonal Risk"]
        rows = []
        for d in report_data["disease_risks"]:
            rows.append([
                d.get("crop_type", "N/A"),
                f"{d.get('pest_attack_probability', 0) * 100:.0f}%",
                f"{d.get('disease_outbreak_probability', 0) * 100:.0f}%",
                d.get("seasonal_risk", "N/A"),
            ])
        story.append(_build_data_table(headers, rows))
        story.append(Spacer(1, 12))

    if "recommendations" in report_data:
        rec = report_data["recommendations"]
        story.append(Paragraph("Crop Recommendations", styles["SectionTitle"]))
        if "recommended_crops" in rec:
            story.append(Paragraph("Recommended Crops", styles["SubSectionTitle"]))
            headers = ["Crop", "Expected Yield (t/ha)", "Confidence"]
            rows = [
                [c.get("name", "N/A"), f"{c.get('expected_yield', 0):.2f}", f"{c.get('confidence', 0) * 100:.0f}%"]
                for c in rec["recommended_crops"]
            ]
            story.append(_build_data_table(headers, rows))
            story.append(Spacer(1, 8))

        if "fertilizer_plan" in rec:
            story.append(Paragraph("Fertilizer Plan", styles["SubSectionTitle"]))
            fp = rec["fertilizer_plan"]
            fp_details = [
                ["Nitrogen (kg/ha)", str(fp.get("nitrogen", "N/A"))],
                ["Phosphorus (kg/ha)", str(fp.get("phosphorus", "N/A"))],
                ["Potassium (kg/ha)", str(fp.get("potassium", "N/A"))],
                ["Schedule", fp.get("schedule", "N/A")],
            ]
            story.append(_build_data_table(["Component", "Value"], fp_details))
            story.append(Spacer(1, 8))

        if "irrigation_schedule" in rec:
            story.append(Paragraph("Irrigation Schedule", styles["SubSectionTitle"]))
            irr = rec["irrigation_schedule"]
            irr_details = [
                ["Frequency (days)", str(irr.get("frequency_days", "N/A"))],
                ["Amount per Session (mm)", str(irr.get("amount_per_session", "N/A"))],
                ["Total Requirement (mm)", str(irr.get("total_requirement", "N/A"))],
                ["Method", irr.get("method", "N/A")],
            ]
            story.append(_build_data_table(["Parameter", "Value"], irr_details))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=ReportBranding.LIGHT_GRAY))
    story.append(Paragraph(
        f"This comprehensive report was generated by {ReportBranding.COMPANY_NAME}. "
        "All predictions are based on historical climate data and machine learning models. "
        "Actual agricultural outcomes may vary.",
        styles["Footer"],
    ))

    doc.build(story, onFirstPage=_create_header, onLaterPages=_create_header)
    return filepath
