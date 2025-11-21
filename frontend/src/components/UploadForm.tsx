import { useRef, useState, type ChangeEvent, type DragEvent } from "react";

interface Props {
  disabled: boolean;
  onFileSelected: (file: File) => Promise<void> | void;
  uploadedFileName: string | null;
}

function UploadForm({ disabled, onFileSelected, uploadedFileName }: Props) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null;
    setSelectedFile(file);
    if (file) {
      void triggerUpload(file);
    }
  };

  const triggerUpload = async (file: File) => {
    setUploading(true);
    try {
      await onFileSelected(file);
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0] ?? null;
    setSelectedFile(file);
    if (file) {
      if (fileInputRef.current) {
        fileInputRef.current.files = event.dataTransfer.files;
      }
      void triggerUpload(file);
    }
    setIsDragging(false);
  };

  return (
    <form onSubmit={(event) => event.preventDefault()} style={{ display: "grid", gap: "1rem" }}>
      <label
        style={{
          padding: "1.5rem",
          border: isDragging ? "2px solid #2563eb" : "2px dashed #cbd5f5",
          borderRadius: "12px",
          textAlign: "center",
          background: isDragging ? "#e0edff" : "transparent",
          transition: "border 0.2s ease, background 0.2s ease",
        }}
        onClick={() => fileInputRef.current?.click()}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".yaml,.yml,.json"
          onChange={handleFileChange}
          style={{ display: "none" }}
        />
        <p style={{ margin: 0 }}>
          {selectedFile?.name || uploadedFileName || "Drag & drop or click to upload OpenAPI spec"}
        </p>
        <small style={{ color: uploadedFileName ? "#16a34a" : "#94a3b8" }}>
          {uploadedFileName ? "✅ OpenAPI loaded" : uploading ? "Uploading..." : ".yaml or .json"}
        </small>
      </label>
    </form>
  );
}

export default UploadForm;
