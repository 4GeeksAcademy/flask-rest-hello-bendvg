#!/usr/bin/env python
"""Generate ER diagram from SQLAlchemy models"""
from models import db, Usuario, Personaje, Planeta, Favorito, Post, Comentario
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


# Create minimal Flask app for SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import models

# Initialize db
db.init_app(app)

# Generate diagram within app context
with app.app_context():
    try:
        from sqlalchemy_schemadisplay import create_schema_graph

        print("Generando diagrama de la base de datos...")
        graph = create_schema_graph(
            metadata=db.metadata,
            engine=db.engine,
            show_indexes=True,
            rankdir='LR'
        )
        graph.write_png('diagram.png')
        print("✓ diagram.png generado exitosamente!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
