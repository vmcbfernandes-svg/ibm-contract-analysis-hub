# Hugging Face Spaces Deployment Guide

This application is configured for deployment on Hugging Face Spaces using Docker.

## Quick Deploy

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in:
   - **Space name:** `ibm-contract-analysis-hub`
   - **Description:** IBM TLS Offerings Contract Analysis Hub
   - **License:** MIT
   - **SDK:** Docker
   - **Hardware:** CPU Basic (Free)
4. Click "Create Space"
5. Connect your GitHub repository: `vmcbfernandes-svg/ibm-contract-analysis-hub`
6. The app will automatically build and deploy

## Configuration

The Dockerfile is configured to:
- Run on port 7860 (Hugging Face Spaces standard)
- Use Python 3.11
- Install all dependencies from requirements.txt
- Run Streamlit in headless mode
- Include health checks

## Access

Once deployed, your app will be available at:
`https://huggingface.co/spaces/vitorfernandes1969/ibm-contract-analysis-hub`

## Features

- ✅ Free hosting
- ✅ Automatic builds from GitHub
- ✅ Can be set to private
- ✅ No usage limits
- ✅ Persistent URL

## Troubleshooting

If the build fails:
1. Check the build logs in Hugging Face Spaces
2. Verify all files are pushed to GitHub
3. Ensure requirements.txt has all dependencies
4. Check Dockerfile syntax

## Support

For issues with Hugging Face Spaces:
- Documentation: https://huggingface.co/docs/hub/spaces
- Community: https://discuss.huggingface.co/