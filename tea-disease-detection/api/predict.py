from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import io
import base64

app = Flask(__name__)

# Disease information database
DISEASE_INFO = {
    'blister_blight': {
        'name': 'Blister Blight',
        'severity_levels': {
            'low': {
                'description': 'Early stage infection with few lesions',
                'treatment': [
                    'Apply copper-based fungicide (0.5% Bordeaux mixture)',
                    'Spray early morning or late evening',
                    'Remove and destroy infected leaves',
                    'Improve air circulation by pruning'
                ],
                'timing': 'Apply treatment within 24-48 hours',
                'cost': 'Low - ₹200-300 per acre'
            },
            'medium': {
                'description': 'Moderate infection spreading across multiple leaves',
                'treatment': [
                    'Apply systemic fungicide (Hexaconazole 5% EC @ 2ml/L)',
                    'Repeat application after 10-12 days',
                    'Remove heavily infected shoots',
                    'Avoid overhead irrigation'
                ],
                'timing': 'Immediate treatment required',
                'cost': 'Medium - ₹500-700 per acre'
            },
            'high': {
                'description': 'Severe infection with widespread damage',
                'treatment': [
                    'Emergency spray with combination fungicide',
                    'Apply Copper Oxychloride 50% WP @ 3g/L + Hexaconazole',
                    'Prune infected areas aggressively',
                    'Apply at 7-day intervals for 3 weeks',
                    'Consult local agricultural extension officer'
                ],
                'timing': 'Urgent - treat within 24 hours',
                'cost': 'High - ₹1000-1500 per acre'
            }
        }
    },
    'red_rust': {
        'name': 'Red Rust',
        'severity_levels': {
            'low': {
                'description': 'Few orange-red spots on leaf undersides',
                'treatment': [
                    'Apply Copper Oxychloride 50% WP @ 2.5g/L',
                    'Ensure proper drainage in field',
                    'Remove infected leaves manually',
                    'Maintain plant spacing for air flow'
                ],
                'timing': 'Apply within 2-3 days',
                'cost': 'Low - ₹150-250 per acre'
            },
            'medium': {
                'description': 'Multiple rust pustules spreading',
                'treatment': [
                    'Apply Propiconazole 25% EC @ 1ml/L',
                    'Spray both leaf surfaces thoroughly',
                    'Repeat after 14 days',
                    'Avoid water stress'
                ],
                'timing': 'Apply immediately',
                'cost': 'Medium - ₹400-600 per acre'
            },
            'high': {
                'description': 'Severe rust covering large leaf areas',
                'treatment': [
                    'Apply Tridemorph 80% EC @ 1ml/L',
                    'Combine with copper fungicide',
                    'Apply at 7-10 day intervals',
                    'Improve field sanitation',
                    'Consider resistant variety replacement'
                ],
                'timing': 'Urgent treatment needed',
                'cost': 'High - ₹800-1200 per acre'
            }
        }
    },
    'brown_blight': {
        'name': 'Brown Blight',
        'severity_levels': {
            'low': {
                'description': 'Small brown spots on few leaves',
                'treatment': [
                    'Apply Mancozeb 75% WP @ 2.5g/L',
                    'Remove infected leaves',
                    'Avoid leaf wetness periods',
                    'Apply preventive spray'
                ],
                'timing': 'Apply within 48 hours',
                'cost': 'Low - ₹200-350 per acre'
            },
            'medium': {
                'description': 'Brown lesions spreading to stems',
                'treatment': [
                    'Apply Carbendazim 50% WP @ 1g/L',
                    'Alternate with Copper fungicide',
                    'Spray at 10-day intervals',
                    'Improve drainage and reduce humidity'
                ],
                'timing': 'Immediate action required',
                'cost': 'Medium - ₹500-800 per acre'
            },
            'high': {
                'description': 'Extensive browning and leaf drop',
                'treatment': [
                    'Emergency treatment with Azoxystrobin 23% SC @ 1ml/L',
                    'Prune severely infected areas',
                    'Apply combination fungicide',
                    'Improve overall plant health with foliar nutrition',
                    'Seek expert consultation'
                ],
                'timing': 'Critical - immediate treatment',
                'cost': 'High - ₹1000-1800 per acre'
            }
        }
    },
    'healthy': {
        'name': 'Healthy Leaf',
        'severity_levels': {
            'none': {
                'description': 'No disease detected - leaf is healthy',
                'treatment': [
                    'Continue regular monitoring',
                    'Apply preventive fungicide during monsoon',
                    'Maintain proper nutrition (NPK balance)',
                    'Ensure good field hygiene'
                ],
                'timing': 'Preventive care - monitor weekly',
                'cost': 'Preventive - ₹100-200 per acre'
            }
        }
    }
}

# Simple rule-based classification (for demo - replace with actual trained model)
def classify_disease(img_array):
    """
    This is a simplified classifier for demonstration.
    In production, replace this with your trained model.
    """
    # Calculate color features
    mean_rgb = np.mean(img_array, axis=(0, 1))
    
    # Simple rule-based classification (placeholder logic)
    # In real implementation, use a trained CNN model
    
    # Mock classification based on color analysis
    r, g, b = mean_rgb
    
    # Blister blight - tends to have yellowish-brown spots
    if g > r and g > b and np.std(img_array) > 30:
        disease = 'blister_blight'
        confidence = 0.75 + np.random.random() * 0.2
        severity = 'medium' if np.std(img_array) > 40 else 'low'
    # Red rust - orange-red coloration
    elif r > g and r > b and r > 100:
        disease = 'red_rust'
        confidence = 0.70 + np.random.random() * 0.25
        severity = 'high' if r > 140 else 'medium' if r > 120 else 'low'
    # Brown blight - brown spots
    elif abs(r - g) < 20 and r < 100 and np.std(img_array) > 25:
        disease = 'brown_blight'
        confidence = 0.72 + np.random.random() * 0.23
        severity = 'medium' if np.std(img_array) > 35 else 'low'
    else:
        disease = 'healthy'
        confidence = 0.80 + np.random.random() * 0.15
        severity = 'none'
    
    return disease, severity, confidence

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Get image from request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        # Read and process image
        img = Image.open(file.stream)
        
        # Resize to standard size
        img = img.resize((224, 224))
        img_array = np.array(img)
        
        # Classify disease
        disease, severity, confidence = classify_disease(img_array)
        
        # Get disease information
        disease_data = DISEASE_INFO[disease]
        severity_data = disease_data['severity_levels'][severity]
        
        # Prepare response
        response = {
            'success': True,
            'disease': disease_data['name'],
            'disease_key': disease,
            'severity': severity.capitalize(),
            'confidence': round(confidence * 100, 2),
            'description': severity_data['description'],
            'treatment': severity_data['treatment'],
            'timing': severity_data['timing'],
            'estimated_cost': severity_data['cost'],
            'additional_tips': [
                'Monitor the affected area daily',
                'Keep records of treatments applied',
                'Contact local agricultural extension for expert advice',
                'Consider weather forecast - avoid spraying before rain'
            ]
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Tea Leaf Disease Detection API',
        'version': '1.0.0'
    })

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Return list of detectable diseases"""
    diseases = []
    for key, value in DISEASE_INFO.items():
        if key != 'healthy':
            diseases.append({
                'key': key,
                'name': value['name']
            })
    return jsonify(diseases)

# For local testing
if __name__ == '__main__':
    app.run(debug=True, port=5000)
