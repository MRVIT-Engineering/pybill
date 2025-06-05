from weasyprint import HTML # type: ignore
from datetime import datetime, timedelta
from mrvbill.utils.fs import read_from_config
from pathlib import Path
import calendar

def generate_invoice_pdf(time_entries, month: str, name: str = None, customer: dict = None, vat: bool = False):
    # Calculate totals
    total_hours = sum(float(entry['hours']) for entry in time_entries)
    rate_per_hour = float(read_from_config('vendor_rate_per_hour'))
    subtotal = total_hours * rate_per_hour
    vat_rate = 0.19  # 19% VAT in Romania
    vat_amount = subtotal * vat_rate
    total = subtotal + vat_amount if customer['vat'] else subtotal

    # Get invoice number and format it with leading zeros
    invoice_number = int(read_from_config('invoice_series_number'))
    formatted_invoice_number = f"{invoice_number:04d}"  # This will format numbers as 0001, 0012, etc.
    
    # Calculate the last day of the month
    current_year = datetime.now().year
    month_number = datetime.strptime(month, '%B').month
    last_day = calendar.monthrange(current_year, month_number)[1]
    invoice_date = datetime(current_year, month_number, last_day)
    
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
                .logo {{
                    width: 100px;
                    height: auto;
                    margin-bottom: 20px;
                }}
                .company-info {{
                    display: flex;
                    align-items: flex-start;
                }}
                .logo-container {{
                    margin-right: 20px;
                }}
                .totals-table {{
                    width: 300px;
                    margin-left: auto;
                    margin-top: 20px;
                }}
                .totals-table td {{
                    padding: 5px;
                }}
                .totals-table .amount {{
                    text-align: right;
                }}
            </style>
        </head>
        <body>
            <div class="company-info">
                <div class="logo-container">
                    <img src="{read_from_config('vendor_logo')}" class="logo" />
                </div>
                <div>
                    <div class="invoice-header">INVOICE</div>
                </div>
            </div>
            
            <div class="invoice-meta">
                <div>Series {read_from_config('invoice_series_name')} no. {formatted_invoice_number} dated {invoice_date.strftime('%d/%m/%Y')}</div>
                <div>Payment term {(invoice_date + timedelta(days=30)).strftime('%d/%m/%Y')}</div>
            </div>

            <div class="vendor-customer-section">
                <div class="vendor-section">
                    <div class="section-title">VENDOR</div>
                    <div>{read_from_config('vendor_name')}</div>
                    <div>{read_from_config('account_number')}</div>
                    <div>VAT CODE: {read_from_config('vendor_vat_code')}</div>
                    <div>No. Registrar of Companies: {read_from_config('vendor_national_trade_register_no')}</div>
                    <div>Address: {read_from_config('vendor_address')}</div>
                    <div>State/Province: {read_from_config('vendor_city')}</div>
                    <div>Country: {read_from_config('vendor_country')}</div>
                </div>

                <div class="customer-section">
                    <div class="section-title">CUSTOMER</div>
                    <div>{customer['name']}</div>
                    <div>Address: {customer['address']}</div>
                    <div>Country: {customer['country']}</div>
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
                    <td>{subtotal:.2f}</td>
                </tr>
            </table>

            <div class="totals-table">
                <table>
                    <tr>
                        <td>Subtotal USD:</td>
                        <td class="amount">{subtotal:.2f}</td>
                    </tr>
                   
                    <tr>
                        <td><strong>Total USD:</strong></td>
                        <td class="amount"><strong>{total:.2f}</strong></td>
                    </tr>
                </table>
            </div>


        </body>
    </html>
    """

    # Generate PDF file
    output_dir = Path(read_from_config('invoices_folder'))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_name = name if name else f"invoice_{read_from_config('invoice_series_name')}_{formatted_invoice_number}_{month.lower()}_{datetime.now().strftime('%Y%m%d')}"
    output_file = output_dir / f"{file_name}.pdf"
    
    HTML(string=html_content).write_pdf(str(output_file))
    return str(output_file)