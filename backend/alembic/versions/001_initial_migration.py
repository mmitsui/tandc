"""Initial migration: create documents and summaries tables

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create documents table
    op.create_table(
        'documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('service_name', sa.String(), nullable=False),
        sa.Column('document_type', sa.String(), nullable=False),
        sa.Column('raw_content', sa.Text(), nullable=False),
        sa.Column('content_hash', sa.String(), nullable=False),
        sa.Column('extracted_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f('ix_documents_url'), 'documents', ['url'], unique=False)
    op.create_index(op.f('ix_documents_service_name'), 'documents', ['service_name'], unique=False)
    op.create_index(op.f('ix_documents_content_hash'), 'documents', ['content_hash'], unique=False)
    
    # Create summaries table
    op.create_table(
        'summaries',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('red_flags', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('rules', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('concessions', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('clarity_score', sa.Integer(), nullable=False),
        sa.Column('reading_level', sa.String(), nullable=False),
        sa.Column('original_word_count', sa.Integer(), nullable=False),
        sa.Column('summary_word_count', sa.Integer(), nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('model_version', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_summaries_document_id'), 'summaries', ['document_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_summaries_document_id'), table_name='summaries')
    op.drop_table('summaries')
    op.drop_index(op.f('ix_documents_content_hash'), table_name='documents')
    op.drop_index(op.f('ix_documents_service_name'), table_name='documents')
    op.drop_index(op.f('ix_documents_url'), table_name='documents')
    op.drop_table('documents')
