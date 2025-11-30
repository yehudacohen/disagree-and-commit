"""ZIP packager for bundling spec documents and uploading to S3."""

import zipfile
import boto3
from io import BytesIO
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
import os


@dataclass
class SpecPackage:
    """Generated spec package."""
    feature_name: str
    requirements_md: str
    design_md: str
    tasks_md: str


@dataclass
class PackageResult:
    """Result of packaging operation."""
    zip_key: str
    download_url: str
    expires_at: str
    feature_name: str


class ZipPackager:
    """Bundles spec documents into ZIP and uploads to S3."""
    
    def __init__(self, s3_bucket: Optional[str] = None):
        """
        Initialize the ZipPackager.
        
        Args:
            s3_bucket: S3 bucket name for uploads. If None, uses local storage.
        """
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket or os.environ.get('SPEC_BUCKET', 'disagree-commit-specs')
    
    def package(self, spec: SpecPackage, session_id: str = "") -> PackageResult:
        """
        Create ZIP and upload to S3.
        
        Args:
            spec: Generated spec documents
            session_id: Optional session ID for naming
            
        Returns:
            PackageResult with download URL
        """
        # Create ZIP in memory
        zip_buffer = self.create_zip(spec)
        
        # Generate S3 key
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        zip_key = f"specs/{spec.feature_name}_{timestamp}.zip"
        
        # Upload to S3
        self.upload_to_s3(zip_buffer, zip_key)
        
        # Generate presigned URL
        download_url = self.generate_presigned_url(zip_key)
        
        # Calculate expiration
        expires_at = (datetime.utcnow() + timedelta(hours=24)).isoformat()
        
        return PackageResult(
            zip_key=zip_key,
            download_url=download_url,
            expires_at=expires_at,
            feature_name=spec.feature_name
        )
    
    def create_zip(self, spec: SpecPackage) -> BytesIO:
        """
        Create in-memory ZIP file with folder structure.
        
        Structure:
        .kiro/
          specs/
            {feature-name}/
              requirements.md
              design.md
              tasks.md
        """
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            base_path = f".kiro/specs/{spec.feature_name}"
            
            # Add requirements.md
            zf.writestr(f"{base_path}/requirements.md", spec.requirements_md)
            
            # Add design.md
            zf.writestr(f"{base_path}/design.md", spec.design_md)
            
            # Add tasks.md
            zf.writestr(f"{base_path}/tasks.md", spec.tasks_md)
        
        zip_buffer.seek(0)
        return zip_buffer
    
    def upload_to_s3(self, zip_buffer: BytesIO, key: str) -> None:
        """Upload ZIP to S3 assets bucket."""
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=zip_buffer.getvalue(),
                ContentType='application/zip'
            )
        except Exception as e:
            raise RuntimeError(f"Failed to upload to S3: {e}")
    
    def generate_presigned_url(self, key: str, expiration: int = 86400) -> str:
        """Generate presigned URL with 24-hour expiration."""
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            raise RuntimeError(f"Failed to generate presigned URL: {e}")
    
    def create_local_zip(self, spec: SpecPackage, output_dir: str = ".") -> str:
        """
        Create ZIP file locally (for testing without S3).
        
        Args:
            spec: Generated spec documents
            output_dir: Directory to save ZIP file
            
        Returns:
            Path to created ZIP file
        """
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        zip_path = os.path.join(output_dir, f"{spec.feature_name}_{timestamp}.zip")
        
        zip_buffer = self.create_zip(spec)
        
        with open(zip_path, 'wb') as f:
            f.write(zip_buffer.getvalue())
        
        return zip_path
