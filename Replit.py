import sys
import pandas as pd
import datacompy
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QTabWidget, QComboBox,
    QLineEdit, QMessageBox, QFrame, QScrollArea, QHeaderView, QSplitter,
    QWizard, QWizardPage, QRadioButton, QButtonGroup, QGroupBox, QCheckBox,
    QListWidget, QListWidgetItem, QTextEdit, QProgressBar, QGraphicsDropShadowEffect,
    QDialog, QProgressDialog, QFormLayout)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QFont, QPalette, QColor
import sqlite3

# Design System - Modern Color Palette
COLORS = {
    'background': '#F5F7FA',
    'surface': '#FFFFFF',
    'primary': '#2563EB',
    'primary_hover': '#1D4ED8',
    'secondary': '#10B981',
    'danger': '#EF4444',
    'warning': '#F59E0B',
    'info': '#3B82F6',
    'purple': '#8B5CF6',
    'text_primary': '#1F2937',
    'text_secondary': '#6B7280',
    'border': '#E5E7EB',
    'shadow': 'rgba(0, 0, 0, 0.1)'
}


class DatabaseCredentialsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Database Connection")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # Info label
        info_label = QLabel("Enter database connection details:")
        info_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        layout.addWidget(info_label)
        
        # Form layout for inputs
        form = QFormLayout()
        form.setSpacing(12)
        
        # Database type
        self.db_type_combo = QComboBox()
        self.db_type_combo.addItems(["SQLite (Local)", "PostgreSQL", "MySQL"])
        self.db_type_combo.currentIndexChanged.connect(self.on_db_type_changed)
        form.addRow("Database Type:", self.db_type_combo)
        
        # Host
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("localhost")
        self.host_input.setText("localhost")
        form.addRow("Host:", self.host_input)
        
        # Port
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("5432")
        self.port_input.setText("5432")
        form.addRow("Port:", self.port_input)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("username")
        form.addRow("Username:", self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("password")
        form.addRow("Password:", self.password_input)
        
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #E5E7EB;
                color: #374151;
                padding: 10px 24px;
                border-radius: 8px;
                font-weight: 600;
                border: none;
            }
            QPushButton:hover {
                background-color: #D1D5DB;
            }
        """)
        button_layout.addWidget(cancel_btn)
        
        connect_btn = QPushButton("Connect")
        connect_btn.clicked.connect(self.accept)
        connect_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                padding: 10px 24px;
                border-radius: 8px;
                font-weight: 600;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
        """)
        button_layout.addWidget(connect_btn)
        
        layout.addLayout(button_layout)
        
        # Set SQLite as default (hide server fields)
        self.on_db_type_changed(0)
    
    def on_db_type_changed(self, index):
        # SQLite doesn't need host/port/username/password
        is_sqlite = index == 0
        self.host_input.setVisible(not is_sqlite)
        self.port_input.setVisible(not is_sqlite)
        self.username_input.setVisible(not is_sqlite)
        self.password_input.setVisible(not is_sqlite)
    
    def get_credentials(self):
        db_type_map = {0: 'sqlite', 1: 'postgresql', 2: 'mysql'}
        return {
            'db_type': db_type_map[self.db_type_combo.currentIndex()],
            'host': self.host_input.text(),
            'port': self.port_input.text(),
            'username': self.username_input.text(),
            'password': self.password_input.text()
        }


class MetricCard(QFrame):

    def __init__(self, title, value, subtitle="", color="#3b82f6"):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.NoFrame)

        # Main layout directly on the frame
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']}; 
            font-size: 11px; 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 0.5px;
            background: transparent;
        """)
        layout.addWidget(title_label)

        # Value
        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"""
            color: {color}; 
            font-size: 36px; 
            font-weight: 800;
            background: transparent;
            margin-top: 8px;
        """)
        layout.addWidget(value_label)

        # Subtitle
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet(f"""
                color: {COLORS['text_secondary']}; 
                font-size: 12px; 
                font-weight: 400;
                background: transparent;
            """)
            subtitle_label.setWordWrap(True)
            layout.addWidget(subtitle_label)

        layout.addStretch()

        # Modern design with clean white background and subtle shadow
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-radius: 12px;
                border: 1px solid {COLORS['border']};
            }}
            QFrame:hover {{
                border: 1px solid {color};
                background-color: {COLORS['surface']};
            }}
        """)

        # Add drop shadow for depth
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 25))
        self.setGraphicsEffect(shadow)

        self.setMinimumHeight(160)
        self.setMaximumHeight(200)
        self.setMinimumWidth(220)
        self.setMaximumWidth(260)


class DataSourcePage(QWizardPage):

    def __init__(self, dataset_type):
        super().__init__()
        self.dataset_type = dataset_type
        self.setTitle(f"Step 1: Select {dataset_type.title()} Dataset Source")
        self.setSubTitle(
            f"Choose how you want to load your {dataset_type} dataset")

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Source selection
        source_group = QGroupBox("Data Source")
        source_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #374151;
            }
        """)
        source_layout = QVBoxLayout()

        self.source_group = QButtonGroup()

        self.csv_radio = QRadioButton("📄 CSV File")
        self.csv_radio.setStyleSheet("font-size: 14px; padding: 10px;")
        self.csv_radio.setChecked(True)

        self.sql_radio = QRadioButton("🗄️ SQL Database")
        self.sql_radio.setStyleSheet("font-size: 14px; padding: 10px;")

        self.source_group.addButton(self.csv_radio, 1)
        self.source_group.addButton(self.sql_radio, 2)

        source_layout.addWidget(self.csv_radio)
        source_layout.addWidget(self.sql_radio)
        source_group.setLayout(source_layout)

        layout.addWidget(source_group)
        layout.addStretch()

        self.setLayout(layout)

        self.registerField(f"{dataset_type}_source", self.csv_radio)


class DataLoadPage(QWizardPage):

    def __init__(self, dataset_type):
        super().__init__()
        self.dataset_type = dataset_type
        self.df = None
        self.setTitle(f"Step 2: Load {dataset_type.title()} Dataset")
        self.setSubTitle(f"Select and preview your {dataset_type} data")

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # File/DB selection area
        load_frame = QFrame()
        load_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        load_layout = QVBoxLayout(load_frame)

        # CSV section
        self.csv_widget = QWidget()
        csv_layout = QVBoxLayout(self.csv_widget)

        csv_btn_layout = QHBoxLayout()
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setStyleSheet(
            "color: #6b7280; font-style: italic;")
        csv_btn_layout.addWidget(self.file_path_label)

        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_csv)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
        """)
        csv_btn_layout.addWidget(self.browse_btn)
        csv_layout.addLayout(csv_btn_layout)

        # SQL section
        self.sql_widget = QWidget()
        sql_layout = QVBoxLayout(self.sql_widget)

        # Database name input
        db_name_label = QLabel("Database Name:")
        db_name_label.setStyleSheet("font-weight: 600;")
        sql_layout.addWidget(db_name_label)

        self.db_name_input = QLineEdit()
        self.db_name_input.setPlaceholderText("Enter database name (e.g., my_database)")
        self.db_name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
            }
        """)
        sql_layout.addWidget(self.db_name_input)

        sql_query_label = QLabel("SQL Query:")
        sql_query_label.setStyleSheet("font-weight: 600; margin-top: 10px;")
        sql_layout.addWidget(sql_query_label)

        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("SELECT * FROM table_name")
        self.query_input.setMaximumHeight(100)
        self.query_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Courier New';
                background-color: white;
            }
        """)
        sql_layout.addWidget(self.query_input)

        self.execute_btn = QPushButton("Connect & Execute Query")
        self.execute_btn.clicked.connect(self.connect_and_execute)
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
        """)
        sql_layout.addWidget(self.execute_btn)
        
        # Store database credentials
        self.db_credentials = None

        self.sql_widget.setVisible(False)

        load_layout.addWidget(self.csv_widget)
        load_layout.addWidget(self.sql_widget)

        layout.addWidget(load_frame)

        # Status
        self.status_label = QLabel("Waiting for data...")
        self.status_label.setStyleSheet(
            "color: #6b7280; font-size: 13px; font-weight: 600;")
        layout.addWidget(self.status_label)

        # Preview table
        preview_label = QLabel("Data Preview:")
        preview_label.setStyleSheet(
            "font-weight: 600; font-size: 14px; margin-top: 10px;")
        layout.addWidget(preview_label)

        self.preview_table = QTableWidget()
        self.preview_table.setMaximumHeight(300)
        self.preview_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f9fafb;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-weight: 600;
            }
        """)
        layout.addWidget(self.preview_table)

        self.setLayout(layout)

    def initializePage(self):
        # Show appropriate widget based on source selection
        source_field = self.field(f"{self.dataset_type}_source")
        if source_field:
            self.csv_widget.setVisible(True)
            self.sql_widget.setVisible(False)
        else:
            self.csv_widget.setVisible(False)
            self.sql_widget.setVisible(True)

    def browse_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "",
                                                   "CSV Files (*.csv)")
        if file_path:
            self.file_path_label.setText(file_path)
            self.load_csv(file_path)

    def connect_and_execute(self):
        db_name = self.db_name_input.text().strip()
        query = self.query_input.toPlainText().strip()

        if not db_name:
            QMessageBox.warning(self, "Warning", "Please enter a database name.")
            return

        if not query:
            QMessageBox.warning(self, "Warning", "Please enter a SQL query.")
            return

        # Show credentials dialog
        credentials_dialog = DatabaseCredentialsDialog(self)
        if credentials_dialog.exec() == QDialog.DialogCode.Accepted:
            self.db_credentials = credentials_dialog.get_credentials()
            self.execute_query(db_name, query)

    def load_csv(self, file_path):
        progress = QProgressDialog("Loading CSV file...", None, 0, 0, self)
        progress.setWindowTitle("Loading")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        progress.show()
        QApplication.processEvents()
        
        try:
            self.df = pd.read_csv(file_path)
            progress.setValue(100)
            self.update_preview()
            self.status_label.setText(
                f"✅ Loaded: {len(self.df)} rows, {len(self.df.columns)} columns"
            )
            self.status_label.setStyleSheet(
                "color: #10b981; font-weight: 600;")
            self.completeChanged.emit()
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "Error",
                                 f"Failed to load CSV: {str(e)}")
            self.df = None
        finally:
            progress.close()

    def execute_query(self, db_name, query):
        if not self.db_credentials:
            return

        progress = QProgressDialog("Executing SQL query...", None, 0, 0, self)
        progress.setWindowTitle("Running Query")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        progress.show()
        QApplication.processEvents()

        try:
            # Build connection string based on credentials
            creds = self.db_credentials
            
            # For SQLite (local database)
            if creds.get('db_type') == 'sqlite':
                conn = sqlite3.connect(db_name)
            else:
                # For PostgreSQL/MySQL
                try:
                    import sqlalchemy
                    conn_str = ""
                    if creds.get('db_type') == 'postgresql':
                        conn_str = f"postgresql://{creds['username']}:{creds['password']}@{creds['host']}:{creds['port']}/{db_name}"
                    elif creds.get('db_type') == 'mysql':
                        conn_str = f"mysql+pymysql://{creds['username']}:{creds['password']}@{creds['host']}:{creds['port']}/{db_name}"
                    
                    if conn_str:
                        engine = sqlalchemy.create_engine(conn_str)
                        conn = engine.connect()
                    else:
                        raise ValueError("Unsupported database type")
                except ImportError:
                    raise ImportError("SQLAlchemy is required for PostgreSQL/MySQL connections. Install it with: pip install sqlalchemy")
            
            self.df = pd.read_sql_query(query, conn)
            
            if hasattr(conn, 'close'):
                conn.close()
                
            progress.setValue(100)
            self.update_preview()
            self.status_label.setText(
                f"✅ Loaded: {len(self.df)} rows, {len(self.df.columns)} columns"
            )
            self.status_label.setStyleSheet(
                "color: #10b981; font-weight: 600;")
            self.completeChanged.emit()
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "Error",
                                 f"Failed to execute query: {str(e)}")
            self.df = None
        finally:
            progress.close()

    def update_preview(self):
        if self.df is None:
            return

        # Show first 10 rows
        preview_df = self.df.head(10)
        self.preview_table.setRowCount(len(preview_df))
        self.preview_table.setColumnCount(len(preview_df.columns))
        self.preview_table.setHorizontalHeaderLabels(
            preview_df.columns.tolist())

        for i in range(len(preview_df)):
            for j, col in enumerate(preview_df.columns):
                item = QTableWidgetItem(str(preview_df.iloc[i, j]))
                self.preview_table.setItem(i, j, item)

        header = self.preview_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

    def isComplete(self):
        return self.df is not None

    def get_dataframe(self):
        return self.df


class ConfigurationPage(QWizardPage):

    def __init__(self):
        super().__init__()
        self.setTitle("Step 3: Configure Comparison")
        self.setSubTitle("Select join columns and comparison options")

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Join column section
        join_group = QGroupBox("Join Column")
        join_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
        """)
        join_layout = QVBoxLayout()

        join_label = QLabel("Select the column(s) to join datasets on:")
        join_label.setStyleSheet("color: #6b7280; margin-bottom: 5px;")
        join_layout.addWidget(join_label)

        self.join_combo = QComboBox()
        self.join_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
        """)
        join_layout.addWidget(self.join_combo)

        join_group.setLayout(join_layout)
        layout.addWidget(join_group)

        # Compare columns section
        compare_group = QGroupBox("Columns to Compare (Optional)")
        compare_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
        """)
        compare_layout = QVBoxLayout()

        compare_desc = QLabel(
            "Leave empty to compare all columns, or select specific columns:")
        compare_desc.setStyleSheet("color: #6b7280; margin-bottom: 5px;")
        compare_layout.addWidget(compare_desc)

        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all_columns)
        self.clear_all_btn = QPushButton("Clear All")
        self.clear_all_btn.clicked.connect(self.clear_all_columns)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.select_all_btn)
        btn_layout.addWidget(self.clear_all_btn)
        btn_layout.addStretch()
        compare_layout.addLayout(btn_layout)

        self.columns_list = QListWidget()
        self.columns_list.setMaximumHeight(200)
        self.columns_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:hover {
                background-color: #f3f4f6;
            }
        """)
        compare_layout.addWidget(self.columns_list)

        compare_group.setLayout(compare_layout)
        layout.addWidget(compare_group)

        layout.addStretch()
        self.setLayout(layout)

    def initializePage(self):
        wizard = self.wizard()
        if not isinstance(wizard, DataUploadWizard):
            return
        base_df = wizard.base_load_page.get_dataframe()
        compare_df = wizard.compare_load_page.get_dataframe()

        if base_df is not None and compare_df is not None:
            # Find common columns
            common_cols = list(set(base_df.columns) & set(compare_df.columns))
            self.join_combo.clear()
            self.join_combo.addItems(sorted(common_cols))

            # Populate columns list with checkboxes
            self.columns_list.clear()
            for col in sorted(common_cols):
                item = QListWidgetItem()
                item.setText(col)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.columns_list.addItem(item)

    def select_all_columns(self):
        for i in range(self.columns_list.count()):
            item = self.columns_list.item(i)
            if item:
                item.setCheckState(Qt.CheckState.Checked)

    def clear_all_columns(self):
        for i in range(self.columns_list.count()):
            item = self.columns_list.item(i)
            if item:
                item.setCheckState(Qt.CheckState.Unchecked)

    def get_selected_columns(self):
        selected = []
        for i in range(self.columns_list.count()):
            item = self.columns_list.item(i)
            if item and item.checkState() == Qt.CheckState.Checked:
                selected.append(item.text())
        return selected if selected else None

    def isComplete(self):
        return self.join_combo.currentText() != ""


class SummaryPage(QWizardPage):

    def __init__(self):
        super().__init__()
        self.setTitle("Step 4: Review and Compare")
        self.setSubTitle("Review your settings and start the comparison")

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Summary frame
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 8px;
                padding: 20px;
                border: 1px solid #e5e7eb;
            }
        """)
        summary_layout = QVBoxLayout(summary_frame)

        summary_title = QLabel("📋 Configuration Summary")
        summary_title.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #111827; margin-bottom: 10px;"
        )
        summary_layout.addWidget(summary_title)

        self.summary_text = QLabel()
        self.summary_text.setWordWrap(True)
        self.summary_text.setStyleSheet(
            "color: #374151; font-size: 13px; line-height: 1.6;")
        summary_layout.addWidget(self.summary_text)

        layout.addWidget(summary_frame)

        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                text-align: center;
                background-color: white;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #3b82f6;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel()
        self.status_label.setStyleSheet(
            "color: #6b7280; font-weight: 600; margin-top: 5px;")
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setLayout(layout)

    def initializePage(self):
        wizard = self.wizard()
        if not isinstance(wizard, DataUploadWizard):
            return
        base_df = wizard.base_load_page.get_dataframe()
        compare_df = wizard.compare_load_page.get_dataframe()

        if base_df is None or compare_df is None:
            return

        join_col = wizard.config_page.join_combo.currentText()
        selected_cols = wizard.config_page.get_selected_columns()

        summary = f"""
        <b>Base Dataset:</b> {len(base_df)} rows, {len(base_df.columns)} columns<br>
        <b>Compare Dataset:</b> {len(compare_df)} rows, {len(compare_df.columns)} columns<br>
        <b>Join Column:</b> {join_col}<br>
        <b>Columns to Compare:</b> {len(selected_cols) if selected_cols else 'All common columns'} columns
        """

        if selected_cols:
            summary += f"<br><b>Selected Columns:</b> {', '.join(selected_cols[:5])}"
            if len(selected_cols) > 5:
                summary += f" and {len(selected_cols) - 5} more..."

        self.summary_text.setText(summary)


class DataUploadWizard(QWizard):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Data Comparison Wizard")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setFixedSize(800, 650)

        self.setStyleSheet("""
            QWizard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #eff6ff, stop:1 white);
            }
            QWizard QLabel {
                color: #1e40af;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 700;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
            QRadioButton {
                color: #1e40af;
                font-size: 14px;
                font-weight: 600;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #3b82f6;
            }
            QRadioButton::indicator:checked {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                    fx:0.5, fy:0.5, stop:0 #3b82f6, stop:1 #2563eb);
                border: 2px solid #1e40af;
            }
            QComboBox, QLineEdit, QTextEdit {
                padding: 10px;
                border: 2px solid #bfdbfe;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                color: #1e40af;
            }
            QComboBox:hover, QLineEdit:hover, QTextEdit:hover {
                border: 2px solid #3b82f6;
            }
            QComboBox:focus, QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #2563eb;
                background-color: #eff6ff;
            }
            QGroupBox {
                font-weight: 700;
                font-size: 14px;
                color: #1e40af;
                border: 2px solid #bfdbfe;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 12px;
                background: white;
            }
            QGroupBox::title {
                color: #2563eb;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
            }
            QListWidget {
                border: 2px solid #bfdbfe;
                border-radius: 8px;
                background-color: white;
                padding: 8px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 6px;
                color: #1e40af;
            }
            QListWidget::item:hover {
                background-color: #eff6ff;
            }
            QListWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
            QTableWidget {
                border: 2px solid #bfdbfe;
                border-radius: 8px;
                background-color: white;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                padding: 10px;
                border: none;
                font-weight: 700;
            }
        """)

        # Create pages
        self.base_source_page = DataSourcePage('base')
        self.base_load_page = DataLoadPage('base')
        self.compare_source_page = DataSourcePage('compare')
        self.compare_load_page = DataLoadPage('compare')
        self.config_page = ConfigurationPage()
        self.summary_page = SummaryPage()

        # Add pages
        self.addPage(self.base_source_page)
        self.addPage(self.base_load_page)
        self.addPage(self.compare_source_page)
        self.addPage(self.compare_load_page)
        self.addPage(self.config_page)
        self.addPage(self.summary_page)

        self.setButtonText(QWizard.WizardButton.FinishButton, "Run Comparison")


class DataCompyGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.base_df: Optional[pd.DataFrame] = None
        self.compare_df: Optional[pd.DataFrame] = None
        self.comparison: Optional[datacompy.Compare] = None
        self.base_load_page: Optional[DataLoadPage] = None
        self.compare_load_page: Optional[DataLoadPage] = None
        self.config_page: Optional[ConfigurationPage] = None

        self.setWindowTitle("DataCompy Analytics Dashboard")
        self.setGeometry(100, 100, 1400, 900)
        self.setup_ui()

    def setup_ui(self):
        # Set modern blue and white color scheme with improved styling
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f1f5f9, stop:1 #e0e7ff);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px 28px;
                font-weight: 700;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1d4ed8, stop:1 #1e40af);
            }
            QLabel {
                color: #1e293b;
                font-size: 14px;
                background: transparent;
            }
            QTabWidget::pane {
                border: 2px solid #cbd5e1;
                border-radius: 16px;
                background-color: white;
                margin-top: -1px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f1f5f9, stop:1 #e2e8f0);
                color: #64748b;
                padding: 14px 28px;
                margin-right: 4px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                font-weight: 700;
                font-size: 13px;
                border: 2px solid transparent;
            }
            QTabBar::tab:selected {
                background: white;
                color: #3b82f6;
                border: 2px solid #cbd5e1;
                border-bottom-color: white;
            }
            QTabBar::tab:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e0e7ff, stop:1 #c7d2fe);
                color: #3b82f6;
            }
            QTableWidget {
                border: 2px solid #cbd5e1;
                border-radius: 12px;
                background-color: white;
                gridline-color: #f1f5f9;
                selection-background-color: #dbeafe;
                selection-color: #1e40af;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:alternate {
                background-color: #f8fafc;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                padding: 14px;
                border: none;
                font-weight: 800;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 14px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #60a5fa);
                border-radius: 7px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #3b82f6);
            }
            QScrollBar:horizontal {
                background: #f1f5f9;
                height: 14px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #60a5fa);
                border-radius: 7px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #3b82f6);
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                border: none;
                background: none;
            }
        """)

        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: {COLORS['background']};")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Modern Header with clean design - compact
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-radius: 12px;
                border: 1px solid {COLORS['border']};
                padding: 16px 24px;
            }}
        """)
        
        # Add subtle shadow to header
        header_shadow = QGraphicsDropShadowEffect()
        header_shadow.setBlurRadius(15)
        header_shadow.setXOffset(0)
        header_shadow.setYOffset(2)
        header_shadow.setColor(QColor(0, 0, 0, 20))
        header_frame.setGraphicsEffect(header_shadow)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setSpacing(16)

        # App title
        title_container = QVBoxLayout()
        title_container.setSpacing(4)
        
        header = QLabel("📊 DataCompy Analytics")
        header.setStyleSheet(f"""
            font-size: 22px; 
            font-weight: 700; 
            color: {COLORS['text_primary']};
            background: transparent;
        """)
        title_container.addWidget(header)
        
        subtitle = QLabel("Compare and analyze your datasets with precision")
        subtitle.setStyleSheet(f"""
            font-size: 12px; 
            color: {COLORS['text_secondary']};
            background: transparent;
        """)
        title_container.addWidget(subtitle)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()

        # New Comparison button with modern styling
        new_btn = QPushButton("⚡ New Comparison")
        new_btn.clicked.connect(self.start_wizard)
        new_btn.setMinimumHeight(48)
        new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                font-size: 14px;
                border-radius: 10px;
                font-weight: 700;
                padding: 12px 28px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
            QPushButton:pressed {{
                background-color: #1E40AF;
            }}
        """)
        header_layout.addWidget(new_btn)

        main_layout.addWidget(header_frame)

        # Status section with modern design
        self.status_frame = QFrame()
        self.status_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-radius: 12px;
                border: 1px solid {COLORS['border']};
                padding: 40px;
            }}
        """)
        status_layout = QVBoxLayout(self.status_frame)

        self.status_label = QLabel("👋 Welcome! Click 'New Comparison' to get started.")
        self.status_label.setStyleSheet(f"""
            font-size: 18px; 
            color: {COLORS['text_secondary']}; 
            font-weight: 600;
            background: transparent;
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.status_label)

        main_layout.addWidget(self.status_frame)

        # Results tabs with modern styling
        self.results_tabs = QTabWidget()
        self.results_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 16px;
            }}
            QTabBar::tab {{
                background-color: transparent;
                color: {COLORS['text_secondary']};
                padding: 12px 24px;
                margin-right: 4px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['surface']};
                color: {COLORS['primary']};
                border-bottom: 3px solid {COLORS['primary']};
            }}
            QTabBar::tab:hover {{
                background-color: {COLORS['border']};
                color: {COLORS['text_primary']};
            }}
        """)
        main_layout.addWidget(self.results_tabs, 1)

    def start_wizard(self):
        wizard = DataUploadWizard(self)

        if wizard.exec() == QWizard.DialogCode.Accepted:
            # Get data from wizard
            assert wizard.base_load_page is not None
            assert wizard.compare_load_page is not None
            assert wizard.config_page is not None

            self.base_df = wizard.base_load_page.get_dataframe()
            self.compare_df = wizard.compare_load_page.get_dataframe()

            assert self.base_df is not None
            assert self.compare_df is not None

            join_col = wizard.config_page.join_combo.currentText()
            selected_cols = wizard.config_page.get_selected_columns()

            self.status_label.setText(
                f"⏳ Running comparison on {len(self.base_df)} base rows and {len(self.compare_df)} compare rows..."
            )
            QApplication.processEvents()

            progress = QProgressDialog("Running comparison analysis...", None, 0, 0, self)
            progress.setWindowTitle("Comparing Data")
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.setMinimumDuration(0)
            progress.setValue(0)
            progress.show()
            QApplication.processEvents()

            try:
                # Run comparison
                self.comparison = datacompy.Compare(self.base_df,
                                                    self.compare_df,
                                                    join_columns=join_col,
                                                    df1_name='Base',
                                                    df2_name='Compare')
                
                progress.setValue(100)
                progress.close()

                # Hide status frame and show results directly
                self.status_frame.hide()
                self.display_results()

            except Exception as e:
                progress.close()
                QMessageBox.critical(self, "Error",
                                     f"Comparison failed: {str(e)}")
                self.status_frame.show()
                self.status_label.setText(f"❌ Comparison failed: {str(e)}")
                self.status_label.setStyleSheet(
                    "font-size: 16px; color: #ef4444; font-weight: 600;")

    def display_results(self):
        self.results_tabs.clear()

        if self.comparison is None or self.base_df is None or self.compare_df is None:
            return

        # Type narrowing assertions
        assert self.base_df is not None
        assert self.compare_df is not None
        assert self.comparison is not None

        # Overview tab with metrics - add scroll area
        overview_scroll = QScrollArea()
        overview_scroll.setWidgetResizable(True)
        overview_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)

        overview_tab = QWidget()
        overview_layout = QVBoxLayout(overview_tab)
        overview_layout.setSpacing(20)
        overview_layout.setContentsMargins(15, 15, 15, 15)
        overview_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        try:
            # Get comparison statistics
            total_rows_base = len(self.base_df)
            total_rows_compare = len(self.compare_df)
            
            # Get the number of rows that exist in both datasets (intersect)
            intersect_rows_df = self.comparison.intersect_rows
            intersect_rows = len(intersect_rows_df) if intersect_rows_df is not None else 0
            
            # Count rows where ALL values match perfectly
            perfectly_matched = self.comparison.count_matching_rows()
            
            # Rows with some differences = rows in common - perfectly matched
            rows_with_differences = intersect_rows - perfectly_matched

            print(
                f"DEBUG: total_rows_base={total_rows_base}, total_rows_compare={total_rows_compare}, intersect_rows={intersect_rows}, perfectly_matched={perfectly_matched}, rows_with_differences={rows_with_differences}"
            )

            # Calculate metrics
            match_rate = (perfectly_matched / intersect_rows * 100) if intersect_rows > 0 else 0

            # Get column counts
            intersect_cols = self.comparison.intersect_columns()
            cols_compared = len(intersect_cols) if intersect_cols else 0

            # Duplicate rows
            join_cols = self.comparison.join_columns if isinstance(
                self.comparison.join_columns,
                list) else [self.comparison.join_columns]
            base_duplicates = self.base_df.duplicated(subset=join_cols).sum()
            compare_duplicates = self.compare_df.duplicated(
                subset=join_cols).sum()

            print(
                f"DEBUG: base_duplicates={base_duplicates}, compare_duplicates={compare_duplicates}"
            )

            # Column statistics
            total_base_cols = len(self.base_df.columns)
            total_compare_cols = len(self.compare_df.columns)
            common_cols = len(intersect_cols) if intersect_cols else 0
            base_only_cols = len(
                set(self.base_df.columns) - set(self.compare_df.columns))
            compare_only_cols = len(
                set(self.compare_df.columns) - set(self.base_df.columns))

            print(
                f"DEBUG: total_base_cols={total_base_cols}, total_compare_cols={total_compare_cols}, common_cols={common_cols}"
            )

            # Calculate column match statistics from comparison data
            cols_with_unequal = 0
            cols_all_equal = 0
            total_unequal_values = 0

            # Get column match info from the comparison object
            for col in intersect_cols:
                if col in join_cols:
                    continue  # Skip join columns
                
                # Check if this column has all values equal
                try:
                    # Count matches from the intersection
                    if intersect_rows_df is not None and not intersect_rows_df.empty:
                        # Get matching values for this column - try both naming conventions
                        base_col = None
                        compare_col = None
                        
                        # Check for _Base/_Compare naming (used by datacompy)
                        if col + '_Base' in intersect_rows_df.columns and col + '_Compare' in intersect_rows_df.columns:
                            base_col = col + '_Base'
                            compare_col = col + '_Compare'
                        # Check for _df1/_df2 naming
                        elif col + '_df1' in intersect_rows_df.columns and col + '_df2' in intersect_rows_df.columns:
                            base_col = col + '_df1'
                            compare_col = col + '_df2'
                        
                        if base_col and compare_col:
                            matches = (intersect_rows_df[base_col].astype(str) == intersect_rows_df[compare_col].astype(str)).sum()
                            mismatches = len(intersect_rows_df) - matches
                            
                            if mismatches > 0:
                                cols_with_unequal += 1
                                total_unequal_values += mismatches
                            else:
                                cols_all_equal += 1
                except Exception as e:
                    print(f"DEBUG: Error processing column {col}: {e}")
            
            print(
                f"DEBUG: cols_all_equal={cols_all_equal}, cols_with_unequal={cols_with_unequal}, total_unequal_values={total_unequal_values}"
            )

            # Create all metric cards in a scrollable area without section headers
            cards_scroll = QScrollArea()
            cards_scroll.setWidgetResizable(True)
            cards_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            cards_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            cards_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
            
            cards_widget = QWidget()
            cards_widget.setStyleSheet("background: transparent;")
            cards_main_layout = QVBoxLayout(cards_widget)
            cards_main_layout.setSpacing(16)
            cards_main_layout.setContentsMargins(0, 0, 0, 0)
            
            # Create all cards
            all_cards = []
            
            # Row statistics cards
            all_cards.append(MetricCard("Total Rows (Base)", total_rows_base, 
                              f"Compare: {total_rows_compare} rows", "#3b82f6"))
            all_cards.append(MetricCard("Perfectly Matched", perfectly_matched,
                              f"{match_rate:.1f}% of common rows", "#10b981"))
            all_cards.append(MetricCard("Rows w/ Differences", rows_with_differences,
                              f"Out of {intersect_rows} common", "#ef4444"))
            all_cards.append(MetricCard("Base Duplicates", base_duplicates,
                              f"Compare: {compare_duplicates} dupes", "#8b5cf6"))
            
            # Column statistics cards
            all_cards.append(MetricCard("Base Columns", total_base_cols,
                                  f"Compare: {total_compare_cols} cols", "#3b82f6"))
            all_cards.append(MetricCard("Common Columns", common_cols,
                                  "In both datasets", "#10b981"))
            all_cards.append(MetricCard("Base Only Cols", base_only_cols,
                                  "Exclusive to base", "#f59e0b"))
            all_cards.append(MetricCard("Compare Only Cols", compare_only_cols,
                                  "Exclusive to compare", "#f97316"))
            
            # Column value comparison cards
            all_cards.append(MetricCard("Columns Equal", cols_all_equal,
                                  "All values match", "#10b981"))
            all_cards.append(MetricCard("Columns Unequal", cols_with_unequal,
                                  "Some values differ", "#f97316"))
            all_cards.append(MetricCard("Unequal Values", total_unequal_values,
                                  "Total differences", "#ef4444"))
            
            if cols_compared > 0:
                col_match_pct = (cols_all_equal / cols_compared * 100)
                all_cards.append(MetricCard("Column Match %", f"{col_match_pct:.1f}%",
                                      "Columns fully matching", "#6366f1"))
            
            # Arrange cards in rows - 4 cards per row
            cards_per_row = 4
            for i in range(0, len(all_cards), cards_per_row):
                row_layout = QHBoxLayout()
                row_layout.setSpacing(16)
                
                for card in all_cards[i:i+cards_per_row]:
                    row_layout.addWidget(card)
                
                # Add stretch to the last row if it's not full
                if len(all_cards[i:i+cards_per_row]) < cards_per_row:
                    row_layout.addStretch()
                
                cards_main_layout.addLayout(row_layout)
            
            cards_main_layout.addStretch()
            cards_scroll.setWidget(cards_widget)
            overview_layout.addWidget(cards_scroll)

        except Exception as e:
            error_label = QLabel(f"Error calculating metrics: {str(e)}")
            error_label.setStyleSheet("color: #ef4444; padding: 10px;")
            overview_layout.addWidget(error_label)

        self.results_tabs.addTab(overview_tab, "📊 Overview")
        
        # Summary tab
        self.add_summary_tab()

        # Column analysis
        self.add_column_analysis_tab()

        # Mismatch details
        self.add_mismatch_tab()

        # Unique records
        self.add_unique_records_tab()

    def add_summary_tab(self):
        summary_tab = QWidget()
        summary_tab.setStyleSheet("background: white;")
        summary_layout = QVBoxLayout(summary_tab)
        summary_layout.setContentsMargins(20, 20, 20, 20)
        summary_layout.setSpacing(16)
        
        # Summary text
        summary_scroll = QScrollArea()
        summary_scroll.setWidgetResizable(True)
        summary_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        summary_widget = QWidget()
        summary_widget.setStyleSheet("background: transparent;")
        summary_content_layout = QVBoxLayout(summary_widget)

        try:
            if self.comparison is None:
                raise ValueError("No comparison data available")
            report_text = self.comparison.report()
            summary_label = QLabel(report_text)
            summary_label.setWordWrap(True)
            summary_label.setStyleSheet(f"""
                font-family: 'Courier New'; 
                font-size: 12px; 
                padding: 15px; 
                background-color: {COLORS['surface']};
                color: {COLORS['text_primary']};
                border-radius: 8px;
                border: 1px solid {COLORS['border']};
            """)
            summary_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse)
            summary_content_layout.addWidget(summary_label)
        except Exception as e:
            error_label = QLabel(f"Error generating report: {str(e)}")
            error_label.setStyleSheet("color: #ef4444; padding: 10px;")
            summary_content_layout.addWidget(error_label)

        summary_scroll.setWidget(summary_widget)
        summary_layout.addWidget(summary_scroll)
        
        self.results_tabs.addTab(summary_tab, "📝 Summary")

    def add_column_analysis_tab(self):
        tab = QWidget()
        tab.setStyleSheet("background: white;")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        if self.comparison is None or self.base_df is None or self.compare_df is None:
            error_label = QLabel("No comparison data available")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(error_label)
            self.results_tabs.addTab(tab, "📋 Column Analysis")
            return

        # Type narrowing assertions
        assert self.base_df is not None
        assert self.compare_df is not None
        assert self.comparison is not None

        # Summary stats at top
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #eff6ff, stop:1 #dbeafe);
                border-radius: 16px;
                border: 2px solid #93c5fd;
                padding: 20px;
            }
        """)
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setSpacing(32)

        all_cols = set(self.base_df.columns) | set(self.compare_df.columns)
        intersect = set(self.comparison.intersect_columns())
        matched_cols = len(intersect)
        base_only = len(
            set(self.base_df.columns) - set(self.compare_df.columns))
        compare_only = len(
            set(self.compare_df.columns) - set(self.base_df.columns))

        match_label = QLabel(f"✅ Matched: {matched_cols}")
        match_label.setStyleSheet(
            "color: #10b981; font-size: 18px; font-weight: 800; background: transparent;"
        )
        summary_layout.addWidget(match_label)

        base_only_label = QLabel(f"🔵 Base Only: {base_only}")
        base_only_label.setStyleSheet(
            "color: #3b82f6; font-size: 18px; font-weight: 800; background: transparent;"
        )
        summary_layout.addWidget(base_only_label)

        compare_only_label = QLabel(f"🟠 Compare Only: {compare_only}")
        compare_only_label.setStyleSheet(
            "color: #f59e0b; font-size: 18px; font-weight: 800; background: transparent;"
        )
        summary_layout.addWidget(compare_only_label)

        total_label = QLabel(f"📊 Total: {len(all_cols)}")
        total_label.setStyleSheet(
            "color: #6366f1; font-size: 18px; font-weight: 800; background: transparent;"
        )
        summary_layout.addWidget(total_label)

        summary_layout.addStretch()

        layout.addWidget(summary_frame)

        # Column details table
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(
            ["Column", "Status", "Base Type", "Compare Type"])
        header = table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(
                1, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(
                2, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(
                3, QHeaderView.ResizeMode.ResizeToContents)
        table.setAlternatingRowColors(True)

        table.setRowCount(len(all_cols))

        for i, col in enumerate(sorted(all_cols)):
            # Column name
            col_item = QTableWidgetItem(col)
            col_item.setFont(QFont("", 12, QFont.Weight.Bold))
            table.setItem(i, 0, col_item)

            # Status
            if col in intersect:
                status_item = QTableWidgetItem("✓ Matched")
                status_item.setForeground(QColor("#10b981"))
                status_item.setFont(QFont("", 11, QFont.Weight.Bold))
                table.setItem(i, 1, status_item)
            elif col in self.base_df.columns and col not in self.compare_df.columns:
                status_item = QTableWidgetItem("⚠ Base Only")
                status_item.setForeground(QColor("#3b82f6"))
                status_item.setFont(QFont("", 11, QFont.Weight.Bold))
                table.setItem(i, 1, status_item)
            else:
                status_item = QTableWidgetItem("⚠ Compare Only")
                status_item.setForeground(QColor("#f59e0b"))
                status_item.setFont(QFont("", 11, QFont.Weight.Bold))
                table.setItem(i, 1, status_item)

            base_dtype = str(self.base_df[col].dtype
                             ) if col in self.base_df.columns else "N/A"
            compare_dtype = str(self.compare_df[col].dtype
                                ) if col in self.compare_df.columns else "N/A"

            table.setItem(i, 2, QTableWidgetItem(base_dtype))
            table.setItem(i, 3, QTableWidgetItem(compare_dtype))

        table.setSortingEnabled(True)
        layout.addWidget(table)

        self.results_tabs.addTab(tab, "📋 Column Analysis")

    def add_mismatch_tab(self):
        tab = QWidget()
        tab.setStyleSheet("background: white;")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        if self.comparison is None:
            error_label = QLabel("No comparison data available")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(error_label)
            self.results_tabs.addTab(tab, "⚠️ Mismatch Details")
            return

        if not self.comparison.all_mismatch().empty:
            # Get the mismatch data in the new format
            mismatch_df = self.comparison.all_mismatch()

            print(f"DEBUG MISMATCH: columns in all_mismatch = {mismatch_df.columns.tolist()}")
            print(f"DEBUG MISMATCH: shape = {mismatch_df.shape}")

            # Create restructured mismatch table
            mismatch_rows = []
            join_cols = self.comparison.join_columns if isinstance(
                self.comparison.join_columns,
                list) else [self.comparison.join_columns]

            # Get unique column names (extract base names from _Base/_Compare suffixes)
            compare_cols = set()
            for col in mismatch_df.columns:
                if col not in join_cols:
                    if col.endswith('_Base'):
                        compare_cols.add(col[:-5])  # Remove '_Base'
                    elif col.endswith('_Compare'):
                        compare_cols.add(col[:-8])  # Remove '_Compare'

            print(f"DEBUG MISMATCH: compare_cols = {compare_cols}")

            for idx, row in mismatch_df.iterrows():
                # Get join column values
                join_values = [str(row[jc]) for jc in join_cols if jc in row]
                join_value_str = ', '.join(join_values)

                # Check each column for mismatches
                for col in compare_cols:
                    col_base = f"{col}_Base"
                    col_compare = f"{col}_Compare"

                    if col_base in mismatch_df.columns and col_compare in mismatch_df.columns:
                        base_val = row[col_base]
                        compare_val = row[col_compare]

                        # Only add if values are different
                        if str(base_val) != str(compare_val):
                            mismatch_rows.append({
                                'Join Key':
                                join_value_str,
                                'Column Name':
                                col,
                                'Base Value':
                                str(base_val),
                                'Compare Value':
                                str(compare_val)
                            })

            print(f"DEBUG MISMATCH: total mismatch_rows = {len(mismatch_rows)}")

            # Create new DataFrame with restructured data
            if mismatch_rows:
                restructured_df = pd.DataFrame(mismatch_rows)

                # Add count summary at top
                summary_frame = QFrame()
                summary_frame.setStyleSheet("""
                    QFrame {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #fef2f2, stop:1 #fee2e2);
                        border-radius: 16px;
                        border: 2px solid #fca5a5;
                        padding: 20px;
                    }
                """)
                summary_layout = QHBoxLayout(summary_frame)
                summary_layout.setSpacing(32)

                total_mismatches = len(restructured_df)
                unique_keys = restructured_df['Join Key'].nunique()
                unique_cols = restructured_df['Column Name'].nunique()

                mismatch_label = QLabel(
                    f"🔴 Total Mismatches: {total_mismatches}")
                mismatch_label.setStyleSheet(
                    "color: #dc2626; font-size: 18px; font-weight: 800; background: transparent;"
                )
                summary_layout.addWidget(mismatch_label)

                keys_label = QLabel(f"🔑 Affected Keys: {unique_keys}")
                keys_label.setStyleSheet(
                    "color: #dc2626; font-size: 18px; font-weight: 800; background: transparent;"
                )
                summary_layout.addWidget(keys_label)

                cols_label = QLabel(f"📋 Affected Columns: {unique_cols}")
                cols_label.setStyleSheet(
                    "color: #dc2626; font-size: 18px; font-weight: 800; background: transparent;"
                )
                summary_layout.addWidget(cols_label)

                summary_layout.addStretch()

                layout.addWidget(summary_frame)

                # Create the table
                table = QTableWidget()
                table.setRowCount(len(restructured_df))
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(
                    ["Join Key", "Column Name", "Base Value", "Compare Value"])
                header = table.horizontalHeader()
                if header:
                    header.setSectionResizeMode(
                        0, QHeaderView.ResizeMode.ResizeToContents)
                    header.setSectionResizeMode(
                        1, QHeaderView.ResizeMode.ResizeToContents)
                    header.setSectionResizeMode(2,
                                                QHeaderView.ResizeMode.Stretch)
                    header.setSectionResizeMode(3,
                                                QHeaderView.ResizeMode.Stretch)
                table.setAlternatingRowColors(True)

                for i in range(len(restructured_df)):
                    for j, col in enumerate(restructured_df.columns):
                        item = QTableWidgetItem(str(restructured_df.iloc[i,
                                                                         j]))

                        # Bold font for join key and column name
                        if j < 2:
                            item.setFont(QFont("", 11, QFont.Weight.Bold))

                        # Color code the values (Base and Compare)
                        if j >= 2:
                            item.setBackground(QColor("#fef2f2"))
                            item.setForeground(QColor("#dc2626"))
                            item.setFont(QFont("", 11, QFont.Weight.Bold))

                        table.setItem(i, j, item)

                table.setSortingEnabled(True)
                layout.addWidget(table)
            else:
                self._add_no_mismatch_message(layout)
        else:
            self._add_no_mismatch_message(layout)

        self.results_tabs.addTab(tab, "⚠️ Mismatch Details")

    def _add_no_mismatch_message(self, layout):
        message_frame = QFrame()
        message_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f0fdf4, stop:1 #dcfce7);
                border-radius: 16px;
                border: 2px solid #86efac;
                padding: 40px;
            }
        """)
        message_layout = QVBoxLayout(message_frame)

        icon_label = QLabel("✅")
        icon_label.setStyleSheet("font-size: 64px; background: transparent;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_layout.addWidget(icon_label)

        label = QLabel("No mismatches found!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            "font-size: 24px; color: #10b981; font-weight: 800; background: transparent;"
        )
        message_layout.addWidget(label)

        sublabel = QLabel("All compared records match perfectly")
        sublabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sublabel.setStyleSheet(
            "font-size: 16px; color: #059669; font-weight: 600; background: transparent;"
        )
        message_layout.addWidget(sublabel)

        layout.addWidget(message_frame)

    def add_unique_records_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        if self.comparison is None:
            error_label = QLabel("No comparison data available")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(error_label)
            self.results_tabs.addTab(tab, "🔍 Unique Records")
            return

        splitter = QSplitter(Qt.Orientation.Vertical)

        # Base unique
        base_widget = QWidget()
        base_layout = QVBoxLayout(base_widget)
        base_label = QLabel(
            f"🔵 Unique to Base ({len(self.comparison.df1_unq_rows)} records)")
        base_label.setStyleSheet(
            "font-size: 16px; font-weight: 600; color: #3b82f6; margin: 10px;")
        base_layout.addWidget(base_label)

        if not self.comparison.df1_unq_rows.empty:
            base_table = self.create_table_from_df(
                self.comparison.df1_unq_rows)
            base_layout.addWidget(base_table)
        else:
            no_data = QLabel("No unique records")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            base_layout.addWidget(no_data)

        splitter.addWidget(base_widget)

        # Compare unique
        compare_widget = QWidget()
        compare_layout = QVBoxLayout(compare_widget)
        compare_label = QLabel(
            f"🟢 Unique to Compare ({len(self.comparison.df2_unq_rows)} records)"
        )
        compare_label.setStyleSheet(
            "font-size: 16px; font-weight: 600; color: #10b981; margin: 10px;")
        compare_layout.addWidget(compare_label)

        if not self.comparison.df2_unq_rows.empty:
            compare_table = self.create_table_from_df(
                self.comparison.df2_unq_rows)
            compare_layout.addWidget(compare_table)
        else:
            no_data = QLabel("No unique records")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            compare_layout.addWidget(no_data)

        splitter.addWidget(compare_widget)

        layout.addWidget(splitter)

        self.results_tabs.addTab(tab, "🔍 Unique Records")

    def create_table_from_df(self, df):
        table = QTableWidget()
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns.tolist())
        table.setAlternatingRowColors(True)

        for i in range(len(df)):
            for j, col in enumerate(df.columns):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                table.setItem(i, j, item)

        table.setSortingEnabled(True)
        header = table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            header.setStretchLastSection(True)

        return table


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Set cross-platform font to avoid MS Sans Serif warnings on Linux
    font = QFont("Sans Serif", 10)
    app.setFont(font)

    window = DataCompyGUI()
    window.show()
    sys.exit(app.exec())
