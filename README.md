# FreeFinance — Freelancer Financial Dashboard

A **modern, corporate-grade** React web app designed specifically for freelancers and independent contractors to manage income, expenses, invoices, and generate professional financial reports. All data is stored locally in your browser (IndexedDB) — no backend, no account needed, **100% private and secure**.

## 🎯 Key Features

✅ **Smart Income Tracking** — Log all income with multi-currency support and automatic FX conversion  
✅ **Expense Management** — Track business expenses and automatically calculate tax-deductible amounts  
✅ **Invoice Management** — Create, track, and monitor invoice status with automatic overdue detection  
✅ **Financial Analytics** — Monthly & quarterly rollups based on your fiscal year; trending charts  
✅ **Executive Dashboard** — Interactive charts showing income vs expenses trends and category breakdown  
✅ **Smart Settings** — Configure base currency, fiscal year, categories, payment methods, and FX rates  
✅ **Professional Exports** — Download data as CSV, XLSX, or PDF for your accountant  
✅ **AI Finance Assistant** — Built-in chatbot to answer questions about features and best practices  

## 📋 Pages & Features

| Page | Description |
|------|-------------|
| **Dashboard** | 📊 Real-time income vs. expenses trends, expense category breakdown, KPI cards |
| **Income** | 💵 Log all income with client, category, invoice #, multi-currency FX conversion |
| **Expenses** | 💳 Track expenses by vendor & category; set business use % to auto-calculate deductible |
| **Invoices** | 📄 Issue invoices, track status (Draft/Sent/Paid), automatic overdue detection |
| **Summary** | 📈 Monthly totals for income, expenses, deductible, and net profit; fiscal-year aware |
| **Settings** | ⚙️ Base currency, fiscal year start, custom categories, payment methods, FX rates |
| **Export** | 📥 Download data as CSV, XLSX, or PDF; ready for accountant or tax filing |
| **Finance Assistant** 💬 | AI chatbot to answer questions about features, budgeting, and best practices |

## Installation

### Prerequisites
- Node 16+ (or compatible)
- npm or yarn

### Quick Start

```bash
cd freelancer-finance-dashboard
npm install
npm run dev
```

The app will open automatically at **`http://localhost:3000`**.

## 🚀 Quick Start Guide

### Step 1: Configure Settings ⚙️
- Go to **Settings** page
- Set your **base currency** (USD, EUR, GBP, etc.)
- Choose **fiscal year start month** (important for quarterly reports)
- Add custom **income & expense categories** for your business
- Configure **FX rates** for multi-currency tracking

### Step 2: Record Your Income 💰
- **Income page** → Click "Add Income"
- Fill in: **date**, **client name**, **category**, **amount**, **currency**
- Amount is **automatically converted** to your base currency using FX rates
- Mark as **Paid** once payment is received

### Step 3: Track Your Expenses 💳
- **Expenses page** → Click "Add Expense"
- Fill in: **date**, **vendor**, **category**, **amount**
- Set **business use %** (e.g., 50% for mixed personal/business items)
- **Deductible amount** is automatically calculated

### Step 4: Manage Invoices 📄
- **Invoices page** → Click "Add Invoice"
- Issue invoice with **number**, **client**, **due date**, **amount**
- System automatically **flags overdue invoices**
- Change status to **Paid** when payment received

### Step 5: Review Your Finances 📊
- **Dashboard** → See real-time income vs. expenses trends
- **Summary** → View monthly & quarterly totals, net profit, deductible expenses
- Ask **Finance Assistant** 💬 if you have questions

### Step 6: Export for Your Accountant 📥
- **Export page** → Download as **CSV**, **Excel**, or **PDF**
- Share with accountant for tax filing and planning

6. **Visualize**  
   Dashboard page → view charts of income vs expenses and expense breakdown.

7. **Export**  
   Export page → download CSV, XLSX, or PDF for your accountant.

## Data & Storage

- **All data stored locally** in your browser's IndexedDB
- **No backend** — no logins, no accounts, no tracking
- **Private by design** — your financial data never leaves your computer
- **Portable** — use on any device with a modern browser

## Important Disclaimer

⚠️ **This tool is for organizational purposes only.**

This app is **NOT** tax, legal, or accounting advice. All calculations and reports are provided for reference only.

**You must:**
- Verify all calculations independently
- Consult a qualified tax professional or accountant
- Keep original receipts and documentation
- Follow your local tax laws and regulations

**Limitations:**
- FX rates are static; update manually as needed
- Fiscal year logic is simplified; complex scenarios may need manual adjustment
- Deductible percentages are user-provided; verify with a tax professional

**Use at your own risk.** The creators are not liable for any financial, legal, or tax consequences.

## Technology Stack

- **React** — UI framework
- **React Router** — client-side routing
- **Recharts** — charting library
- **XLSX** — Excel export
- **jsPDF** — PDF generation
- **IndexedDB** — browser local storage
- **Vite** — build tool

## Build for Production

```bash
npm run build
```

This generates an optimized production build in the `dist/` folder.

## Troubleshooting

**Data not persisting?**  
- Check browser IndexedDB support (use Chrome, Firefox, Safari, or Edge)
- Clear browser cache and reload

**Charts not showing?**  
- Ensure you have income/expense data entered
- Check browser console for errors

**Export not working?**  
- Allow pop-ups if blocked by browser
- Check that XLSX/PDF libraries loaded correctly

## License

This project is provided as-is for personal and organizational use.

## Support

For questions or issues, refer to the [Disclaimer](#important-disclaimer) section and consult a financial professional.
