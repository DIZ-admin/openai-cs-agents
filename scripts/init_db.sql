-- ============================================================================
-- ERNI Gruppe Building Agents - Database Initialization Script
-- ============================================================================
-- PostgreSQL database schema for production deployment
-- This script is idempotent and can be run multiple times safely
-- ============================================================================

-- Enable UUID extension for generating unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- CONVERSATIONS TABLE
-- ============================================================================
-- Stores customer conversation sessions
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Customer Information
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    customer_phone VARCHAR(50),
    
    -- Conversation Metadata
    status VARCHAR(50) DEFAULT 'active',
    inquiry_id VARCHAR(100),
    language VARCHAR(10) DEFAULT 'de',
    
    -- Tracking
    last_agent VARCHAR(100),
    message_count INTEGER DEFAULT 0,
    
    CONSTRAINT conversations_status_check CHECK (status IN ('active', 'completed', 'abandoned'))
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_conversations_email ON conversations(customer_email);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversations_status ON conversations(status);
CREATE INDEX IF NOT EXISTS idx_conversations_inquiry_id ON conversations(inquiry_id);

-- ============================================================================
-- MESSAGES TABLE
-- ============================================================================
-- Stores individual messages within conversations
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Message Content
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    
    -- Metadata
    agent_name VARCHAR(100),
    tool_calls JSONB,
    guardrail_triggered BOOLEAN DEFAULT false,
    
    CONSTRAINT messages_role_check CHECK (role IN ('user', 'assistant', 'system', 'tool'))
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_messages_role ON messages(role);

-- ============================================================================
-- PROJECTS TABLE
-- ============================================================================
-- Stores building project information
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_number VARCHAR(50) UNIQUE NOT NULL,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Project Details
    project_type VARCHAR(100),
    construction_type VARCHAR(100),
    area_sqm DECIMAL(10,2),
    location VARCHAR(255),
    budget_chf DECIMAL(12,2),
    preferred_start_date DATE,
    
    -- Project Status
    status VARCHAR(50) DEFAULT 'inquiry',
    progress INTEGER DEFAULT 0,
    current_stage VARCHAR(100),
    next_milestone VARCHAR(255),
    
    -- Responsible Person
    project_manager VARCHAR(255),
    architect VARCHAR(255),
    
    CONSTRAINT projects_status_check CHECK (status IN ('inquiry', 'planning', 'approved', 'production', 'assembly', 'finishing', 'completed', 'cancelled')),
    CONSTRAINT projects_progress_check CHECK (progress >= 0 AND progress <= 100),
    CONSTRAINT projects_type_check CHECK (project_type IN ('Einfamilienhaus', 'Mehrfamilienhaus', 'Agrar', 'Renovation', 'Other')),
    CONSTRAINT projects_construction_check CHECK (construction_type IN ('Holzbau', 'Systembau', 'Mixed'))
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_projects_number ON projects(project_number);
CREATE INDEX IF NOT EXISTS idx_projects_conversation ON projects(conversation_id);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_created_at ON projects(created_at DESC);

-- ============================================================================
-- CONSULTATIONS TABLE
-- ============================================================================
-- Stores consultation appointments with specialists
CREATE TABLE IF NOT EXISTS consultations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Consultation Details
    specialist_type VARCHAR(100) NOT NULL,
    specialist_name VARCHAR(255),
    consultation_date DATE NOT NULL,
    consultation_time TIME NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    
    -- Location
    location VARCHAR(255) DEFAULT 'ERNI Gruppe, Guggibadstrasse 8, 6288 Schongau',
    meeting_type VARCHAR(50) DEFAULT 'in-person',
    
    -- Status
    status VARCHAR(50) DEFAULT 'scheduled',
    
    -- Customer Confirmation
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    customer_phone VARCHAR(50),
    confirmation_sent BOOLEAN DEFAULT false,
    reminder_sent BOOLEAN DEFAULT false,
    
    -- Notes
    notes TEXT,
    
    CONSTRAINT consultations_specialist_check CHECK (specialist_type IN ('Architekt', 'Holzbau-Ingenieur', 'Bauleiter', 'Planner', 'Engineer')),
    CONSTRAINT consultations_status_check CHECK (status IN ('scheduled', 'confirmed', 'completed', 'cancelled', 'no-show')),
    CONSTRAINT consultations_meeting_type_check CHECK (meeting_type IN ('in-person', 'video', 'phone'))
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_consultations_conversation ON consultations(conversation_id);
CREATE INDEX IF NOT EXISTS idx_consultations_date ON consultations(consultation_date);
CREATE INDEX IF NOT EXISTS idx_consultations_specialist ON consultations(specialist_type);
CREATE INDEX IF NOT EXISTS idx_consultations_status ON consultations(status);
CREATE INDEX IF NOT EXISTS idx_consultations_email ON consultations(customer_email);

-- ============================================================================
-- COST ESTIMATES TABLE
-- ============================================================================
-- Stores cost estimation history
CREATE TABLE IF NOT EXISTS cost_estimates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Project Parameters
    project_type VARCHAR(100) NOT NULL,
    construction_type VARCHAR(100) NOT NULL,
    area_sqm DECIMAL(10,2) NOT NULL,
    
    -- Cost Calculation
    base_price_per_sqm DECIMAL(10,2) NOT NULL,
    min_cost_chf DECIMAL(12,2) NOT NULL,
    max_cost_chf DECIMAL(12,2) NOT NULL,
    
    -- Metadata
    calculation_method VARCHAR(100) DEFAULT 'standard',
    notes TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_cost_estimates_conversation ON cost_estimates(conversation_id);
CREATE INDEX IF NOT EXISTS idx_cost_estimates_created_at ON cost_estimates(created_at DESC);

-- ============================================================================
-- AUDIT LOG TABLE
-- ============================================================================
-- Stores audit trail for compliance and debugging
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Event Details
    event_type VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id UUID,
    
    -- User/Agent Information
    user_id VARCHAR(255),
    agent_name VARCHAR(100),
    
    -- Event Data
    event_data JSONB,
    ip_address INET,
    user_agent TEXT,
    
    -- Result
    success BOOLEAN DEFAULT true,
    error_message TEXT
);

-- Indexes for audit queries
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_event_type ON audit_log(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_log_entity ON audit_log(entity_type, entity_id);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Trigger to update updated_at timestamp on conversations
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_consultations_updated_at
    BEFORE UPDATE ON consultations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger to increment message count on conversations
CREATE OR REPLACE FUNCTION increment_message_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversations
    SET message_count = message_count + 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.conversation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER increment_conversation_message_count
    AFTER INSERT ON messages
    FOR EACH ROW
    EXECUTE FUNCTION increment_message_count();

-- ============================================================================
-- INITIAL DATA (Optional)
-- ============================================================================

-- Insert sample project statuses for testing (can be removed in production)
-- Uncomment the following lines if you want sample data

/*
INSERT INTO projects (project_number, project_type, construction_type, area_sqm, location, status, progress, current_stage, next_milestone, project_manager)
VALUES 
    ('2024-156', 'Einfamilienhaus', 'Holzbau', 150.00, 'Muri', 'production', 75, 'Production', 'Assembly 15-19 May 2025', 'Tobias Wili'),
    ('2024-089', 'Mehrfamilienhaus', 'Holzbau', 320.00, 'Schongau', 'planning', 40, 'Planning', 'Building permit submission 10 June 2025', 'André Arnold'),
    ('2023-234', 'Agrar', 'Systembau', 500.00, 'Hochdorf', 'completed', 100, 'Completed', 'Final inspection completed', 'Stefan Gisler')
ON CONFLICT (project_number) DO NOTHING;
*/

-- ============================================================================
-- GRANTS (Adjust based on your user setup)
-- ============================================================================

-- Grant permissions to erni_user (adjust username as needed)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO erni_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO erni_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO erni_user;

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE 'ERNI Gruppe Building Agents database schema initialized successfully!';
    RAISE NOTICE 'Tables created: conversations, messages, projects, consultations, cost_estimates, audit_log';
    RAISE NOTICE 'Triggers created: update_updated_at, increment_message_count';
END $$;

