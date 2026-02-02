# 🍃 Tea Leaf Disease Detection System

## Overview
An AI-powered web application for early detection of tea leaf diseases in Assam. Helps tea smallholders identify **Blister Blight**, **Red Rust**, and **Brown Blight** with actionable treatment recommendations.

## Features
- 📸 Image upload via smartphone or computer
- 🤖 Automated disease classification
- 📊 Severity level assessment (Low/Medium/High)
- 💊 Detailed treatment recommendations
- 💰 Cost estimates for treatments
- ⏰ Treatment timing guidance
- 📱 Mobile-responsive design

## Diseases Detected
1. **Blister Blight** - Common fungal disease affecting tea leaves
2. **Red Rust** - Orange-red spots on leaf undersides
3. **Brown Blight** - Brown lesions on leaves and stems
4. **Healthy** - No disease detected

## Tech Stack
- **Backend**: Python + Flask
- **Frontend**: HTML, CSS, JavaScript
- **ML**: TensorFlow (extensible for custom models)
- **Deployment**: Vercel Serverless Functions

## Project Structure
```
tea-disease-detection/
├── api/
│   └── predict.py          # Flask API with ML model
├── public/
│   └── index.html          # Frontend interface
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel configuration
└── README.md              # Documentation
```

## Deployment to Vercel

### Prerequisites
- [Vercel Account](https://vercel.com/signup) (free)
- [Vercel CLI](https://vercel.com/cli) (optional)

### Method 1: Deploy via Vercel Dashboard (Easiest)

1. **Push to GitHub**
   ```bash
   cd tea-disease-detection
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration
   - Click "Deploy"

3. **Done!** Your app will be live at `https://your-project.vercel.app`

### Method 2: Deploy via CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd tea-disease-detection
   vercel
   ```

4. **Follow prompts**
   - Set up and deploy: Yes
   - Project name: tea-disease-detection
   - Continue: Yes

5. **Production deployment**
   ```bash
   vercel --prod
   ```

## Local Development

### Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run locally
cd api
python predict.py
```

The app will be available at `http://localhost:5000`

### Testing
1. Open browser to `http://localhost:5000`
2. Upload a tea leaf image
3. Click "Analyze Leaf"
4. View results with treatment recommendations

## Usage Guide

### For Tea Smallholders:
1. Take a clear photo of affected tea leaf
2. Visit the web app on your smartphone
3. Upload the leaf image
4. Receive instant diagnosis and treatment plan
5. Follow the recommended steps and timing
6. Contact local agricultural extension if needed

### Image Guidelines:
- ✅ Clear, well-lit photos
- ✅ Focus on affected areas
- ✅ Capture both sides if possible
- ❌ Avoid blurry images
- ❌ Avoid extreme shadows

## Customization

### Adding a Custom ML Model
Replace the simple classifier in `api/predict.py`:

```python
# Load your trained model
model = tf.keras.models.load_model('your_model.h5')

def classify_disease(img_array):
    # Preprocess image
    img_processed = preprocess_input(img_array)
    img_batch = np.expand_dims(img_processed, axis=0)
    
    # Predict
    predictions = model.predict(img_batch)
    class_idx = np.argmax(predictions[0])
    confidence = predictions[0][class_idx]
    
    # Map to disease names
    diseases = ['blister_blight', 'red_rust', 'brown_blight', 'healthy']
    disease = diseases[class_idx]
    
    return disease, severity, confidence
```

### Updating Treatment Recommendations
Edit the `DISEASE_INFO` dictionary in `api/predict.py`:

```python
DISEASE_INFO = {
    'blister_blight': {
        'name': 'Blister Blight',
        'severity_levels': {
            'low': {
                'description': 'Your description',
                'treatment': ['Step 1', 'Step 2'],
                'timing': 'Your timing',
                'cost': 'Your cost estimate'
            }
            # ... add more severity levels
        }
    }
    # ... add more diseases
}
```

## Limitations & Future Improvements

### Current Limitations:
- Uses simplified rule-based classification (demo purpose)
- Limited to 3 disease types
- Requires good quality images

### Planned Improvements:
- [ ] Train custom CNN model on tea leaf dataset
- [ ] Add more disease types
- [ ] Multi-language support (Assamese, Hindi)
- [ ] Offline mode for low connectivity areas
- [ ] Treatment history tracking
- [ ] Integration with weather data
- [ ] SMS-based alerts

## Training Your Own Model

To improve accuracy, train a custom model:

1. **Collect Dataset**
   - Gather labeled images of tea leaves
   - Categories: blister_blight, red_rust, brown_blight, healthy
   - Minimum 500 images per category

2. **Train Model**
   ```python
   from tensorflow.keras.applications import MobileNetV2
   from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
   from tensorflow.keras.models import Model
   
   # Load base model
   base_model = MobileNetV2(weights='imagenet', include_top=False)
   
   # Add custom layers
   x = base_model.output
   x = GlobalAveragePooling2D()(x)
   x = Dense(128, activation='relu')(x)
   predictions = Dense(4, activation='softmax')(x)
   
   model = Model(inputs=base_model.input, outputs=predictions)
   
   # Train on your dataset
   model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
   model.fit(train_data, epochs=20, validation_data=val_data)
   
   # Save
   model.save('tea_disease_model.h5')
   ```

3. **Deploy Updated Model**
   - Upload model file to your repository
   - Update `predict.py` to load the model
   - Redeploy to Vercel

## Environment Variables

For production, set these in Vercel dashboard:

```
MODEL_PATH=path/to/your/model.h5
DEBUG=false
MAX_IMAGE_SIZE=5242880  # 5MB
```

## API Endpoints

### `POST /api/predict`
Analyze leaf image and return diagnosis.

**Request:**
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
  "success": true,
  "disease": "Blister Blight",
  "severity": "Medium",
  "confidence": 87.5,
  "description": "Moderate infection...",
  "treatment": ["Step 1", "Step 2"],
  "timing": "Apply immediately",
  "estimated_cost": "₹500-700 per acre"
}
```

### `GET /api/health`
Check API status.

### `GET /api/diseases`
List all detectable diseases.

## Support & Contact

For technical issues or questions:
- Create an issue on GitHub
- Contact local agricultural extension officer
- Email: support@example.com

## License
MIT License - Free for educational and commercial use

## Acknowledgments
- Assam Tea Smallholders
- Agricultural Extension Services
- Open source ML community

---

**Built with ❤️ for Assam's Tea Growers**
