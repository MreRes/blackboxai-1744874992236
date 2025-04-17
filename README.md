# WhatsApp Financial Planner Bot

A financial planning assistant that combines a WhatsApp chatbot with a web dashboard for managing personal finances in Indonesia.

## Features

- 💬 WhatsApp Integration
  - Track expenses and income through chat
  - Get instant financial reports
  - Receive personalized financial advice
  - Support for Indonesian language

- 📊 Web Dashboard
  - Real-time financial overview
  - Expense tracking and categorization
  - Income monitoring
  - Savings goals tracking
  - Visual reports and charts

- 💰 Financial Management
  - Expense categorization
  - Income tracking
  - Savings goals
  - Budget planning
  - Financial advice

## Prerequisites

- Python 3.8 or higher
- Chrome browser (for WhatsApp Web automation)
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whatsapp-financial-planner.git
cd whatsapp-financial-planner
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Access the web dashboard:
```
http://localhost:8000
```

3. Scan the WhatsApp QR code when prompted to connect the bot.

## WhatsApp Commands

- Track expense:
```
expense 50000 food lunch
```

- Record income:
```
income 1000000 salary monthly
```

- Check balance:
```
balance
```

- Get financial report:
```
report
```

- Show help:
```
help
```

## Project Structure

```
financial-whatsapp-bot/
├── src/
│   ├── bot/
│   │   ├── whatsapp_handler.py
│   │   └── financial_processor.py
│   ├── dashboard/
│   │   ├── app.py
│   │   └── templates/
│   └── utils/
│       └── config.py
├── main.py
├── requirements.txt
└── README.md
```

## Development

- Run tests:
```bash
pytest
```

- Format code:
```bash
black .
```

- Lint code:
```bash
flake8
```

## Security Notes

- The application uses SQLite for data storage
- WhatsApp session data is stored locally
- Ensure proper security measures when deploying to production
- Use strong passwords and secure environment variables

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Flask and Tailwind CSS
- Uses Selenium for WhatsApp Web automation
- Chart.js for data visualization
