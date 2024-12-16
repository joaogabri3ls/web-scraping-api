from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
from app.scraping.scraper import scrape_espn_news

router = APIRouter()

@router.get("/news", summary="Get news in JSON format")
async def get_news():
    try:
        url = "https://www.espn.com.br/futebol/"
        df = scrape_espn_news(url)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping data: {str(e)}")

@router.get("/news/csv", summary="Download news as CSV")
async def download_csv():
    try:
        url = "https://www.espn.com.br/futebol/"
        df = scrape_espn_news(url)
        csv_file = "news.csv"
        df.to_csv(csv_file, index=False)
        return FileResponse(csv_file, media_type="text/csv", filename="news.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating CSV: {str(e)}")

@router.get("/news/pdf", summary="Download news as PDF")
async def download_pdf():
    try:
        url = "https://www.espn.com.br/futebol/"
        df = scrape_espn_news(url)

        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for _, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['title']} - {row['date']}", ln=True)

        pdf_file = "news.pdf"
        pdf.output(pdf_file)
        return FileResponse(pdf_file, media_type="application/pdf", filename="news.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
