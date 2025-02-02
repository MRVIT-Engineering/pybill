from weasyprint import HTML 
from datetime import datetime, timedelta
from utils.fs import read_from_config

def generate_invoice_pdf(time_entries, month: str, name: str = None):
    # Calculate payment term (30 days from now)
    payment_date = datetime.now() + timedelta(days=30)

    total_hours = 0
    for entry in time_entries:
        total_hours += float(entry['hours'])

    rate_per_hour = read_from_config('VENDOR_RATE_PER_HOUR')
    total_usd = total_hours * rate_per_hour
    

    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                .invoice-header {{ font-size: 24px; color: #4a6584; margin-bottom: 20px; }}
                .invoice-meta {{ 
                    background-color: #4a6584; 
                    color: white; 
                    padding: 10px;
                    display: flex;
                    justify-content: space-between;
                }}
                .vendor-customer-section {{
                    display: flex;
                    justify-content: space-between;
                    margin: 20px 0;
                }}
                .vendor-section, .customer-section {{
                    width: 45%;
                }}
                .section-title {{
                    color: #4a6584;
                    font-size: 14px;
                    margin-bottom: 10px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .total-section {{
                    background-color: #f2f2f2;
                    padding: 10px;
                    text-align: right;
                }}
                .footer {{
                    margin-top: 40px;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="invoice-header">INVOICE</div>
            
            <div class="invoice-meta">
                <div>Series MRVIT no. 0001 dated {datetime.now().strftime('%d/%m/%Y')}</div>
                <div>Payment term {payment_date.strftime('%d/%m/%Y')}</div>
            </div>

            <div class="vendor-customer-section">
                <div class="vendor-section">
                    <div class="section-title">VENDOR</div>
                    <div>{read_from_config('VENDOR_NAME')}</div>
                    <div>VAT CODE: {read_from_config('VENDOR_VAT_CODE')}</div>
                    <div>No. Registrar of Companies: {read_from_config('NATIONAL_TRADE_REGISTER_NO')}</div>
                    <div>Address: {read_from_config('VENDOR_ADDRESS')}</div>
                    <div>State/Province: {read_from_config('VENDOR_CITY')}</div>
                    <div>Country: {read_from_config('VENDOR_COUNTRY')}</div>
                </div>

                <div class="customer-section">
                    <div class="section-title">CUSTOMER</div>
                    <div>MCRO Technology, Inc</div>
                    <div>Address: 1065 Tilman Road, Charlottesville, Virginia, United States</div>
                    <div>State/Province: Virginia</div>
                    <div>Country: United States</div>
                </div>
            </div>

            <div class="section-title">PRODUCTS / SERVICES</div>
            <table>
                <tr>
                    <th>#</th>
                    <th>Description of products/services</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Unit price USD</th>
                    <th>Value USD</th>
                </tr>
                <tr>
                    <td>1</td>
                    <td>Software development services for {month} {datetime.now().year}</td>
                    <td>Point</td>
                    <td>{total_hours}</td>
                    <td>{rate_per_hour:.2f}</td>
                    <td>{total_usd:.2f}</td>
                </tr>
            </table>

            <div class="total-section">
                <div>Total value USD: {total_usd:.2f}</div>
            </div>

            <div class="footer">
                <div>Made by: {read_from_config('VENDOR_NAME')}</div>
            </div>
        </body>
    </html>
    """

    # Generate PDF file
    output_dir = read_from_config('INVOICES_FOLDER')
    file_name = name if name else f"invoice_{month.lower()}_{datetime.now().strftime('%Y%m%d')}"
    output_file = f"{output_dir}/{file_name}.pdf"
    
    HTML(string=html_content).write_pdf(output_file)
    return output_file