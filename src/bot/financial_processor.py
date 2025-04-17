from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import sqlite3
import os

class FinancialProcessor:
    def __init__(self, db_path: str = 'financial.db'):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Initialize the SQLite database and create necessary tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Create savings goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                deadline DATE,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_transaction(self, user_id: int, amount: float, category: str, 
                       transaction_type: str, description: Optional[str] = None) -> bool:
        """Add a new transaction to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO transactions (user_id, amount, category, transaction_type, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, amount, category, transaction_type, description))
            
            conn.commit()
            
            # Update savings goals if it's an income transaction
            if transaction_type == 'income':
                self._process_savings_allocation(user_id, amount)
                
            return True
        except Exception as e:
            print(f"Error adding transaction: {str(e)}")
            return False
        finally:
            conn.close()

    def get_balance(self, user_id: int) -> float:
        """Calculate current balance for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get sum of income
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = ? AND transaction_type = 'income'
            ''', (user_id,))
            total_income = cursor.fetchone()[0]
            
            # Get sum of expenses
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = ? AND transaction_type = 'expense'
            ''', (user_id,))
            total_expenses = cursor.fetchone()[0]
            
            return total_income - total_expenses
        finally:
            conn.close()

    def get_monthly_summary(self, user_id: int, month: Optional[int] = None, 
                          year: Optional[int] = None) -> Dict:
        """Get monthly financial summary"""
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get monthly income
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = ? 
                AND transaction_type = 'income'
                AND strftime('%m', date) = ?
                AND strftime('%Y', date) = ?
            ''', (user_id, f"{month:02d}", str(year)))
            monthly_income = cursor.fetchone()[0]
            
            # Get monthly expenses
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = ? 
                AND transaction_type = 'expense'
                AND strftime('%m', date) = ?
                AND strftime('%Y', date) = ?
            ''', (user_id, f"{month:02d}", str(year)))
            monthly_expenses = cursor.fetchone()[0]
            
            # Get expense breakdown by category
            cursor.execute('''
                SELECT category, SUM(amount) FROM transactions 
                WHERE user_id = ? 
                AND transaction_type = 'expense'
                AND strftime('%m', date) = ?
                AND strftime('%Y', date) = ?
                GROUP BY category
            ''', (user_id, f"{month:02d}", str(year)))
            expense_categories = dict(cursor.fetchall())
            
            return {
                'monthly_income': monthly_income,
                'monthly_expenses': monthly_expenses,
                'savings': monthly_income - monthly_expenses,
                'expense_categories': expense_categories
            }
        finally:
            conn.close()

    def get_savings_goals(self, user_id: int) -> List[Dict]:
        """Get all savings goals for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, target_amount, current_amount, deadline 
                FROM savings_goals 
                WHERE user_id = ?
            ''', (user_id,))
            
            goals = []
            for row in cursor.fetchall():
                goals.append({
                    'id': row[0],
                    'name': row[1],
                    'target_amount': row[2],
                    'current_amount': row[3],
                    'deadline': row[4],
                    'progress': (row[3] / row[2]) * 100 if row[2] > 0 else 0
                })
            
            return goals
        finally:
            conn.close()

    def add_savings_goal(self, user_id: int, name: str, target_amount: float, 
                        deadline: Optional[str] = None) -> bool:
        """Add a new savings goal"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO savings_goals (user_id, name, target_amount, deadline)
                VALUES (?, ?, ?, ?)
            ''', (user_id, name, target_amount, deadline))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding savings goal: {str(e)}")
            return False
        finally:
            conn.close()

    def _process_savings_allocation(self, user_id: int, income_amount: float):
        """Automatically allocate a portion of income to savings goals"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all active savings goals
            cursor.execute('''
                SELECT id, target_amount, current_amount 
                FROM savings_goals 
                WHERE user_id = ? 
                AND current_amount < target_amount
            ''', (user_id,))
            
            goals = cursor.fetchall()
            if not goals:
                return
            
            # Allocate 20% of income among savings goals
            savings_amount = income_amount * 0.2
            allocation_per_goal = savings_amount / len(goals)
            
            for goal_id, target, current in goals:
                # Calculate how much can be added without exceeding target
                remaining = target - current
                to_add = min(allocation_per_goal, remaining)
                
                cursor.execute('''
                    UPDATE savings_goals 
                    SET current_amount = current_amount + ?
                    WHERE id = ?
                ''', (to_add, goal_id))
            
            conn.commit()
        finally:
            conn.close()

    def get_financial_advice(self, user_id: int) -> str:
        """Generate personalized financial advice based on spending patterns"""
        monthly_summary = self.get_monthly_summary(user_id)
        balance = self.get_balance(user_id)
        
        advice = []
        
        # Check income vs expenses ratio
        if monthly_summary['monthly_expenses'] > monthly_summary['monthly_income'] * 0.8:
            advice.append("⚠️ Your expenses are high relative to your income. Consider reducing non-essential spending.")
        
        # Check savings rate
        savings_rate = (monthly_summary['savings'] / monthly_summary['monthly_income'] * 100) if monthly_summary['monthly_income'] > 0 else 0
        if savings_rate < 20:
            advice.append("💡 Try to save at least 20% of your monthly income for long-term financial security.")
        
        # Analyze expense categories
        categories = monthly_summary['expense_categories']
        if 'food' in categories and categories['food'] > monthly_summary['monthly_income'] * 0.3:
            advice.append("🍽️ Your food expenses are high. Consider meal planning or cooking at home more often.")
        
        if 'entertainment' in categories and categories['entertainment'] > monthly_summary['monthly_income'] * 0.2:
            advice.append("🎮 Entertainment expenses are significant. Look for free or low-cost alternatives.")
        
        if not advice:
            advice.append("👍 You're managing your finances well! Keep up the good work!")
        
        return "\n".join(advice)

    def generate_report(self, user_id: int) -> Dict:
        """Generate a comprehensive financial report"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        return {
            'current_balance': self.get_balance(user_id),
            'monthly_summary': self.get_monthly_summary(user_id),
            'savings_goals': self.get_savings_goals(user_id),
            'advice': self.get_financial_advice(user_id)
        }
