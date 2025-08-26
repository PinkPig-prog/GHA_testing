# Model Deployment Automation

This repository contains a GitHub Actions workflow that automatically calls your model registration/update APIs whenever a model becomes available.

## 🚀 Features

- **Automatic Registration**: Registers the `mlt-batch` model when triggered by code changes
- **Manual Updates**: Manually trigger registration or updates via GitHub UI
- **Hardcoded Configuration**: Uses your exact API endpoints and model metadata
- **Real API Integration**: Calls your actual Postman APIs
- **Comprehensive Logging**: Detailed output for debugging and monitoring

## 📁 Repository Structure

```
├── .github/
│   └── workflows/
│       └── model-deployment.yml    # Main GitHub Actions workflow (contains hardcoded model info)
├── model-configs/                  # Example configuration files (for reference)
├── scripts/
│   └── model_deployment.py        # Standalone deployment script (for testing)
└── README.md                      # This documentation
```

## 🛠️ Setup Instructions

### 1. No Setup Required! 🎉

The API doesn't require authentication - the workflow is ready to use immediately!

- **API URL** (hardcoded): `https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager`
- **Authentication**: None required ✅

### 2. Hardcoded Model Configuration

The workflow is currently configured for the `mlt-batch` model with these hardcoded settings:

```json
{
  "model_name": "mlt-batch",
  "variant": "sllim-tg-pkg-300",
  "owner_team": "personalization",
  "omd_business_service": "content-discovery"
}
```

To modify the model information, edit the workflow file directly: `.github/workflows/model-deployment.yml`

### 3. Workflow Triggers

The workflow triggers on:

1. **Push to main**: When any changes are pushed to the main branch (simulating model availability)
2. **Manual trigger**: Via GitHub Actions UI for testing

## 🔧 Usage

### Automatic Deployment

**When model becomes available** (simulated by push to main):
- Push any change to the main branch
- Workflow automatically triggers and **registers** the hardcoded `mlt-batch` model

### Manual Deployment

1. Go to `Actions` tab in your GitHub repository
2. Select "Model Deployment Automation" workflow
3. Click "Run workflow"
4. Select action type:
   - **register**: Register the mlt-batch model (fresh registration)
   - **update**: Update the existing mlt-batch model configuration

### Testing the API Connection

You can test the API connection directly with curl (no authentication needed):

```bash
# Test the API directly
curl -X POST "https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager/v1/models/register" \
     -H "Content-Type: application/json" \
     -d '{"model_name": "test", "variant": "v1.0.0"}'
```

## 📊 API Endpoints

The workflow calls these actual API endpoints:

### Register Model
- **Full URL**: `https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager/v1/models/register`
- **Method**: `POST`
- **Payload**: Complete model configuration (hardcoded in workflow)

### Update Model  
- **Full URL**: `https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager/v1/models/update/CD:personalization:mlt-batch:sllim-tg-pkg-3`
- **Method**: `PUT`
- **Payload**: 
```json
{
  "model": {
    "serving_configuration": {
      // Only serving configuration fields
    }
  }
}
```

## 🔍 Monitoring and Logs

### Viewing Workflow Logs

1. Go to `Actions` tab in your repository
2. Click on the workflow run
3. Expand job steps to view detailed logs

### Log Output Examples

**Successful Registration**:
```
🚀 Registering model: mlt-batch (variant: sllim-tg-pkg-300)
📡 API URL: https://api.example.com/v1/models/register
✅ Model registered successfully!
📄 Response: {"status": "success", "model_id": "..."}
```

**Successful Update**:
```
🔄 Updating model: CD:personalization:mlt-batch:sllim-tg-pkg-3
📡 API URL: https://api.example.com/v1/models/update/CD:personalization:mlt-batch:sllim-tg-pkg-3
✅ Model updated successfully!
```

## 🚨 Troubleshooting

### Common Issues

1. **Model Already Exists Error**
   - This is normal! The workflow handles "already exists" gracefully
   - Each registration uses a unique timestamp variant to avoid conflicts

2. **Model Not Found (Update)**
   - Ensure model was previously registered using the register action
   - The hardcoded model ID is: `CD:personalization:mlt-batch:sllim-tg-pkg-3`

3. **Workflow Not Triggering**
   - For automatic trigger: ensure you're pushing to the `main` branch
   - Check that Actions are enabled in your repository settings

4. **API Connection Issues**
   - Verify the API endpoint is accessible: `https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager`
   - Check if you need VPN access or specific network permissions

### Debugging Steps

1. **Check workflow logs** in GitHub Actions tab
2. **Test API connectivity** manually using curl:
   ```bash
   curl -X POST "https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager/v1/models/register" \
        -H "Content-Type: application/json" \
        -d '{"model_name": "test", "variant": "debug-test"}'
   ```
3. **Check network connectivity** to the API endpoint
4. **Review API response** for detailed error messages

## 🔒 Security Considerations

- No authentication required for the API (public development endpoint)
- Workflow runs on main branch pushes (consider branch protection rules)
- API endpoint is hardcoded in workflow (review before committing)  
- Be cautious when registering models in development environment

## 🛡️ Best Practices

1. **Testing**: Test the workflow manually before relying on automatic triggers
2. **Monitoring**: Set up alerts for workflow failures in GitHub Actions
3. **Version Control**: Document model changes in commit messages
4. **Access Control**: Limit repository access to authorized team members
5. **Environment Awareness**: Remember this connects to a development API endpoint

## 📝 Example Usage

Here's how to use the workflow:

### Automatic Registration (when model becomes available)
```bash
# 1. Make any change to trigger the workflow
echo "Model v1.0.0 is ready" > model-ready.txt

# 2. Commit and push to main
git add model-ready.txt
git commit -m "Model mlt-batch sllim-tg-pkg-300 is available"
git push origin main

# 3. Workflow automatically triggers and registers the hardcoded model
# Check the Actions tab to see the results
```

### Manual Testing
```bash
# 1. Go to GitHub Actions tab
# 2. Select "Model Deployment Automation" workflow  
# 3. Click "Run workflow"
# 4. Choose "register" or "update"
# 5. Click "Run workflow" button
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test using dry-run mode
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.