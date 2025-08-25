from weasyprint import HTML # type: ignore
from datetime import datetime, timedelta
from mrvbill.utils.fs import read_from_config
from pathlib import Path
import calendar

def generate_invoice_pdf(time_entries, month: str, name: str = None, customer: dict = None, series_name: str = None):
    # Calculate totals
    total_hours = sum(float(entry['hours']) for entry in time_entries)
    rate_per_hour = float(read_from_config('vendor_rate_per_hour'))
    subtotal = total_hours * rate_per_hour
    vat_rate = 0.19  # 19% VAT in Romania
    vat_amount = subtotal * vat_rate
    total = subtotal + vat_amount if customer['vat'] else subtotal

    return _generate_invoice_pdf_with_amount(
        total_amount=total,
        month=month,
        name=name,
        customer=customer,
        series_name=series_name,
        quantity=total_hours,
        unit_price=rate_per_hour,
        description=f"Software development services for {month} {datetime.now().year}"
    )

def generate_invoice_pdf_with_amount(amount: float, month: str, customer: dict, service_name: str, currency: str, series: str):
    """
    Generate an invoice PDF with a specified total amount instead of calculating from time entries.
    
    Args:
        amount: The total amount for the invoice
        month: The month for the invoice
        customer: Customer information dict
        service_name: Description of the service/product
        currency: Currency code (e.g., 'USD', 'EUR')
        series: Invoice series name
    """
    return _generate_invoice_pdf_with_amount(
        total_amount=amount,
        month=month,
        name=None,
        customer=customer,
        series_name=series,
        quantity=1,
        unit_price=amount,
        description=service_name,
        currency=currency
    )

def _generate_invoice_pdf_with_amount(total_amount: float, month: str, name: str = None, customer: dict = None, series_name: str = None, quantity: float = 1, unit_price: float = None, description: str = None, currency: str = "USD"):
    """
    Internal method to generate invoice PDF with specified amount and details.
    """
    # Use total_amount as subtotal (before VAT)
    subtotal = total_amount
    vat_rate = 0.19  # 19% VAT in Romania
    vat_amount = subtotal * vat_rate
    total = subtotal + vat_amount if customer.get('vat', False) else subtotal

    series = read_from_config('series')

    print(f"Series: {series}")
    print(f"Series name: {series_name}")
    invoice_number = series[series_name]
    
    # Get invoice number and format it with leading zeros
    formatted_invoice_number = f"{invoice_number:04d}"  # This will format numbers as 0001, 0012, etc.
    
    # Calculate the last day of the month
    current_year = datetime.now().year
    month_number = datetime.strptime(month, '%B').month
    last_day = calendar.monthrange(current_year, month_number)[1]
    invoice_date = datetime(current_year, month_number, last_day)
    
    # Use provided unit_price or calculate it from total_amount and quantity
    display_unit_price = unit_price if unit_price is not None else (total_amount / quantity if quantity > 0 else total_amount)
    
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
                <div>Series {series_name} no. {formatted_invoice_number} dated {invoice_date.strftime('%d/%m/%Y')}</div>
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
                    <th>Unit price {currency}</th>
                    <th>Value {currency}</th>
                </tr>
                <tr>
                    <td>1</td>
                    <td>{description}</td>
                    <td>Point</td>
                    <td>{quantity}</td>
                    <td>{display_unit_price:.2f}</td>
                    <td>{subtotal:.2f}</td>
                </tr>
            </table>

            <div class="totals-table">
                <table>
                    <tr>
                        <td>Subtotal {currency}:</td>
                        <td class="amount">{subtotal:.2f}</td>
                    </tr>
                   
                    <tr>
                        <td><strong>Total {currency}:</strong></td>
                        <td class="amount"><strong>{total:.2f}</strong></td>
                    </tr>
                </table>
            </div>


        </body>
    </html>
    """

    # Generate PDF file

    try:
        output_dir = Path(read_from_config('invoices_folder'))
        print(f"Output directory: {output_dir}")
        print(f"Output directory exists: {output_dir.exists()}")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {output_dir}")

        file_name = name if name else f"invoice_{series_name}_{formatted_invoice_number}_{month.lower()}_{datetime.now().strftime('%Y%m%d')}"
        output_file = output_dir / f"{file_name}.pdf"
        print(f"Output file path: {output_file}")
        
        HTML(string=html_content).write_pdf(str(output_file))
        print(f"PDF generated successfully at: {output_file}")
        return str(output_file)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return None
