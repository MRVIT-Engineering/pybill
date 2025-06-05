# MrvBill CLI

A command-line interface tool for managing bills and time tracking across different providers.

## Features

- Interactive CLI with styled prompts
- Bill management and time tracking
- Customer management
- PDF invoice generation

## Installation

```bash
pipx install mrvbill
```

## Getting Started

After installing the package, you can use the CLI to manage your bills and time tracking by first running the `init` command and going over the setup wizzard.

```bash
bill init
```

This will create a config.json file inside the `root/~/.pybill/config.json` directory that looks like this. You can edit this file manually to change the config. The CLI currenlty only supports the Harvest provider, make sure you don't share your PAT with anyone.

```json
{
  "vendor_name": "Your Company Name",
  "vendor_vat_code": "Your VAT Code",
  "vendor_address": "Your Address",
  "vendor_city": "Your City",
  "vendor_zip": "Your Zip Code",
  "vendor_country": "Your Country",
  "vendor_email": "Your Email",
  "vendor_phone": "Your Phone Number",
  "invoices_folder": "The path to the folder where the invoices will be saved",
  "vendor_currency": "The currency of the invoices",
  "vendor_rate_per_hour": 1000,
  "national_trade_register_no": "Your National Trade Register Number",
  "configured": "1",
  "provider": "harvest",
  "pat": "Your Personal Access Token",
  "account_id": "Your Account ID",
  "invoice_series_name": "The name of the invoice series",
  "invoice_series_number": 1,
  "customers": {}
}
```

## Creating a new customr

```bash
bill create-customer --name "John Doe" --customer-id "123456" --address "123 Main St" --country "United States" --email "john.doe@example.com" --phone "123-456-7890" --vat "1234567890"
```

This will create a new customer and add it in the config.json file. You can create invoices for different customers using the `create` command.

You can also manually add the customer in the config.json `customers` object with a new key value entry. The key should be a unique identifier you choose for the customer.

```json
"customers": {
  "client1": {
    "name": "Client 1",
    "address": "123 Main St",
    "country": "United States",
    "email": "john.doe@example.com",
    "phone": "123-456-7890",
    "vat": "1234567890"
  }
}
```

## Creating an invoice

To create an invoice, you'll need to use the `create` command with the following parameters:

```bash
bill create --month "MonthName" --customer "customer_id" --name "invoice_name"
```

For example:

```bash
bill create --month "January" --customer "client1" --name "invoice_jan_2024"
```

Where:

- `--month`: The month for which you want to create the invoice (e.g., "January", "February", etc.)
- `--customer`: The customer ID that you used when creating the customer (e.g., "client1")
- `--name`: (Optional) A custom name for the invoice file. If not provided, it will use a default format

The command will:

1. Fetch all time entries from Harvest ( or a different provider ) for the specified month
2. Generate a PDF invoice with:
   - Your company details from the config
   - Customer details
   - Time entries and hours worked
   - Subtotal and total amounts (including VAT if applicable)
   - Invoice number and series
   - Payment terms (30 days from invoice date)

The generated PDF will be saved in the invoices folder specified in your config file.

Note: Make sure you have already:

1. Run `bill init` to set up your configuration
2. Created a customer using `bill create-customer` or manually added them to the config file
3. Have time entries logged in Harvest for the specified month
