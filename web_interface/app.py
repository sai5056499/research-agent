#!/usr/bin/env python3
"""
Flask Web Interface for Super Agent & Multi-Agent Research System
Deployable on Vercel
"""

import os
import sys
import json
import asyncio
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import traceback

# Add parent directory to path to import our research modules
sys.path.append(str(Path(__file__).parent.parent))

try:
    from enhanced_super_agent import EnhancedSuperAgent
    from multi_agent_system import MultiAgentSystem
    from integrated_research_system import IntegratedResearchSystem
    from ai_report_generator import AIReportGenerator
except ImportError as e:
    print(f"Warning: Could not import research modules: {e}")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
CORS(app)

# Initialize research systems
try:
    super_agent = EnhancedSuperAgent()
    multi_agent = MultiAgentSystem()
    integrated_system = IntegratedResearchSystem()
    ai_report_generator = AIReportGenerator()
    SYSTEMS_AVAILABLE = True
except Exception as e:
    print(f"Warning: Could not initialize research systems: {e}")
    SYSTEMS_AVAILABLE = False

# Research session storage
research_sessions = {}

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', systems_available=SYSTEMS_AVAILABLE)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'systems_available': SYSTEMS_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/research', methods=['POST'])
def start_research():
    """Start a research session"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        system_type = data.get('system', 'integrated')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        if not SYSTEMS_AVAILABLE:
            return jsonify({'error': 'Research systems not available'}), 503
        
        # Create session ID
        session_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(topic) % 10000}"
        
        # Initialize session
        research_sessions[session_id] = {
            'topic': topic,
            'system': system_type,
            'status': 'starting',
            'progress': 0,
            'start_time': datetime.now().isoformat(),
            'results': None,
            'error': None
        }
        
        # Start research in background thread
        thread = threading.Thread(
            target=run_research_background,
            args=(session_id, topic, system_type)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'session_id': session_id,
            'status': 'started',
            'message': f'Research started for topic: {topic}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_research_background(session_id, topic, system_type):
    """Run research in background thread"""
    try:
        session_data = research_sessions[session_id]
        session_data['status'] = 'running'
        session_data['progress'] = 10
        
        # Run research based on system type
        if system_type == 'super_agent':
            results = asyncio.run(super_agent.perform_advanced_research(topic))
        elif system_type == 'multi_agent':
            results = asyncio.run(multi_agent.perform_comprehensive_research(topic))
        else:  # integrated
            results = asyncio.run(integrated_system.perform_integrated_research(topic))
        
        session_data['progress'] = 90
        session_data['results'] = results
        session_data['status'] = 'completed'
        session_data['progress'] = 100
        session_data['end_time'] = datetime.now().isoformat()
        
    except Exception as e:
        session_data['status'] = 'error'
        session_data['error'] = str(e)
        session_data['progress'] = 0

@app.route('/api/research/<session_id>/status')
def get_research_status(session_id):
    """Get research session status"""
    if session_id not in research_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session_data = research_sessions[session_id]
    return jsonify({
        'session_id': session_id,
        'topic': session_data['topic'],
        'system': session_data['system'],
        'status': session_data['status'],
        'progress': session_data['progress'],
        'start_time': session_data['start_time'],
        'end_time': session_data.get('end_time'),
        'error': session_data.get('error'),
        'has_results': session_data['results'] is not None
    })

@app.route('/api/research/<session_id>/results')
def get_research_results(session_id):
    """Get research results"""
    if session_id not in research_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session_data = research_sessions[session_id]
    
    if session_data['status'] != 'completed':
        return jsonify({'error': 'Research not completed yet'}), 400
    
    if session_data['results'] is None:
        return jsonify({'error': 'No results available'}), 404
    
    # Format results for web display
    results = session_data['results']
    formatted_results = {
        'topic': session_data['topic'],
        'system': session_data['system'],
        'execution_time': session_data.get('end_time'),
        'summary': extract_summary(results),
        'sources': extract_sources(results),
        'insights': extract_insights(results),
        'reports': extract_reports(results),
        'raw_data': results
    }
    
    return jsonify(formatted_results)

@app.route('/api/generate-report', methods=['POST'])
def generate_ai_report():
    """Generate AI report"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        audience = data.get('audience', 'Students, Teachers & Therapists')
        length = data.get('length', 'standard')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        if not SYSTEMS_AVAILABLE:
            return jsonify({'error': 'AI Report Generator not available'}), 503
        
        # Generate report
        report_path = ai_report_generator.generate_report(
            topic=topic,
            audience=audience,
            length=length
        )
        
        # Read report content
        with open(report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        return jsonify({
            'success': True,
            'report_path': report_path,
            'report_content': report_content,
            'topic': topic,
            'audience': audience,
            'length': length
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/systems')
def get_systems():
    """Get available research systems"""
    return jsonify({
        'systems': [
            {
                'id': 'integrated',
                'name': 'Integrated Research System',
                'description': 'Smart system that automatically chooses the best approach',
                'best_for': 'All research types',
                'speed': 'Adaptive'
            },
            {
                'id': 'super_agent',
                'name': 'Super Agent',
                'description': 'Single powerful AI agent for quick research',
                'best_for': 'Quick research, simple topics',
                'speed': 'Fast'
            },
            {
                'id': 'multi_agent',
                'name': 'Multi-Agent System',
                'description': 'Multiple specialized agents for comprehensive analysis',
                'best_for': 'Complex research, detailed analysis',
                'speed': 'Medium'
            }
        ],
        'available': SYSTEMS_AVAILABLE
    })

def extract_summary(results):
    """Extract summary from results"""
    if isinstance(results, dict):
        if 'summary' in results:
            return results['summary']
        elif 'insights' in results and 'key_insights' in results['insights']:
            return results['insights']['key_insights'][:3]
        elif 'extraction_results' in results and 'sites' in results['extraction_results']:
            sites = results['extraction_results']['sites']
            return f"Analyzed {len(sites)} sources with {results['extraction_results'].get('total_content_length', 0)} characters of content"
    return "Research completed successfully"

def extract_sources(results):
    """Extract sources from results"""
    sources = []
    if isinstance(results, dict):
        if 'extraction_results' in results and 'sites' in results['extraction_results']:
            for site in results['extraction_results']['sites']:
                sources.append({
                    'title': site.get('title', 'Unknown'),
                    'url': site.get('url', ''),
                    'content_length': site.get('content_length', 0),
                    'extraction_method': site.get('extraction_method', 'unknown')
                })
    return sources

def extract_insights(results):
    """Extract insights from results"""
    insights = []
    if isinstance(results, dict):
        if 'insights' in results and 'key_insights' in results['insights']:
            insights = results['insights']['key_insights']
        elif 'combined_insights' in results and 'key_insights' in results['combined_insights']:
            insights = results['combined_insights']['key_insights']
    return insights

def extract_reports(results):
    """Extract report paths from results"""
    reports = []
    if isinstance(results, dict):
        if 'ai_reports' in results:
            for report_type, path in results['ai_reports'].items():
                if report_type != 'error':
                    reports.append({
                        'type': report_type.replace('_', ' ').title(),
                        'path': path
                    })
    return reports

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 