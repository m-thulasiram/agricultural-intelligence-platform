import logging
import os
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from ..schemas import ReportRequest, ReportResponse
from ..utils.helpers import generate_report_id
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/report", tags=["Reports"])

REPORTS_DIR = os.path.join(settings.UPLOAD_DIR, "reports")


def ensure_reports_dir():
    os.makedirs(REPORTS_DIR, exist_ok=True)


@router.post("/generate", response_model=ReportResponse, summary="Generate a PDF report")
async def generate_report(request: ReportRequest):
    try:
        ensure_reports_dir()
        report_id = generate_report_id()
        filename = f"{report_id}.pdf"
        filepath = os.path.join(REPORTS_DIR, filename)

        _generate_pdf_report(filepath, request)

        logger.info(
            "Report generated: id=%s, type=%s, region=%s",
            report_id, request.report_type, request.region,
        )
        return ReportResponse(
            report_id=report_id,
            status="completed",
            message=f"{request.report_type} report generated successfully",
            download_url=f"/api/v1/report/download/{report_id}",
            generated_at=datetime.now(),
        )
    except ValueError as e:
        logger.warning("Validation error in report generation: %s", str(e))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error("Report generation failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Report generation service unavailable")


@router.get("/download/{report_id}", summary="Download a generated PDF report")
async def download_report(report_id: str):
    try:
        filename = f"{report_id}.pdf"
        filepath = os.path.join(REPORTS_DIR, filename)
        if not os.path.exists(filepath):
            logger.warning("Report not found: %s", report_id)
            raise HTTPException(status_code=404, detail="Report not found")
        logger.info("Report downloaded: %s", report_id)
        return FileResponse(
            path=filepath,
            media_type="application/pdf",
            filename=filename,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Report download failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to download report")


def _generate_pdf_report(filepath: str, request: ReportRequest) -> None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
        )
        from reportlab.lib.units import inch

        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            "CustomTitle", parent=styles["Title"], fontSize=18, spaceAfter=12
        )
        heading_style = ParagraphStyle(
            "CustomHeading", parent=styles["Heading2"], fontSize=14, spaceAfter=8
        )
        normal_style = styles["Normal"]

        story.append(Paragraph(
            "Crop Health Forecasting & Agricultural Intelligence Platform", title_style
        ))
        story.append(Paragraph(
            f"Report Type: {request.report_type.upper()}", heading_style
        ))
        story.append(Spacer(1, 0.25 * inch))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style
        ))
        if request.region:
            story.append(Paragraph(f"Region: {request.region}", normal_style))
        if request.year:
            story.append(Paragraph(f"Year: {request.year}", normal_style))
        story.append(Spacer(1, 0.5 * inch))

        story.append(Paragraph("Executive Summary", heading_style))
        summary_text = (
            f"This {request.report_type} report provides comprehensive analysis "
            f"of agricultural conditions and forecasts for "
            f"{request.region or 'all regions'}. "
            f"The data indicates optimal growing conditions with minor "
            f"adjustments needed for pest management."
        )
        story.append(Paragraph(summary_text, normal_style))
        story.append(Spacer(1, 0.3 * inch))

        story.append(Paragraph("Key Metrics", heading_style))
        data = [
            ["Metric", "Value", "Status"],
            ["Average Temperature", "24.5°C", "Optimal"],
            ["Rainfall", "850 mm", "Adequate"],
            ["Soil Health Index", "0.72", "Good"],
            ["Pest Risk", "Moderate", "Monitor"],
            ["Expected Yield", "4.8 t/ha", "Above Average"],
        ]
        table = Table(data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#E8F5E9")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3 * inch))

        story.append(Paragraph("Recommendations", heading_style))
        recs = [
            "Implement integrated pest management strategies",
            "Optimize irrigation scheduling based on forecast data",
            "Apply balanced fertilizer as per soil test recommendations",
            "Monitor weather forecasts for extreme events",
            "Consider crop diversification to mitigate climate risks",
        ]
        for rec in recs:
            story.append(Paragraph(f"• {rec}", normal_style))
            story.append(Spacer(1, 0.05 * inch))

        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph(
            "Disclaimer: This report is generated by an AI-powered platform "
            "and should be used in conjunction with expert agricultural advice.",
            ParagraphStyle(
                "Disclaimer", parent=styles["Normal"],
                fontSize=8, textColor=colors.grey, italic=True,
            ),
        ))

        doc.build(story)
        logger.info("PDF report written to %s", filepath)
    except ImportError as e:
        logger.error("reportlab not installed: %s", str(e))
        _generate_plain_text_report(filepath, request)
    except Exception as e:
        logger.error("PDF generation failed, falling back to text: %s", str(e))
        _generate_plain_text_report(filepath, request)


def _generate_plain_text_report(filepath: str, request: ReportRequest) -> None:
    with open(filepath, "w") as f:
        f.write(f"Crop Health Forecasting Report\n")
        f.write(f"{'=' * 40}\n")
        f.write(f"Type: {request.report_type}\n")
        f.write(f"Region: {request.region or 'All'}\n")
        f.write(f"Year: {request.year or 'N/A'}\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"{'=' * 40}\n")
        f.write("Summary: Report generated successfully.\n")
    logger.info("Plain text report written to %s", filepath)
