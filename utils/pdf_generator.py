from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(country, growth, inflation):

    file_name = "Executive_Trade_Report.pdf"

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    story = []

    content = f"""
    Global Trade Intelligence Report

    Country: {country}
    Export Growth: {growth:.2f}%
    Inflation: {inflation:.2f}%

    Executive Summary:
    This country demonstrates measurable export momentum.
    Strategic trade expansion recommended with risk awareness.
    """

    for line in content.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1,12))

    doc.build(story)

    return file_name