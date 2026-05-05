"use client"

import type React from "react"

import { useState } from "react"
import { Upload } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

export function UploadArea() {
  const [isDragging, setIsDragging] = useState(false)
  const [file, setFile] = useState<File | null>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0])
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  }

  return (
    <section className="w-full space-y-4">
      <div className="flex flex-col space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Upload Your Design</h2>
        <p className="text-muted-foreground">Drag and drop your image or click to browse files</p>
      </div>

      <Card
        className={`border-2 border-dashed ${isDragging ? "border-primary bg-primary/5" : "border-muted-foreground/25"} transition-colors duration-200`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <CardContent className="flex flex-col items-center justify-center p-12 text-center">
          <div className="mx-auto flex flex-col items-center justify-center space-y-4">
            <div className="rounded-full bg-muted p-6">
              <Upload className="h-10 w-10 text-muted-foreground" />
            </div>
            <div className="space-y-2">
              <h3 className="text-xl font-semibold">{file ? file.name : "Drop your image here"}</h3>
              <p className="text-sm text-muted-foreground">
                {file
                  ? `${(file.size / 1024 / 1024).toFixed(2)} MB · ${file.type}`
                  : "Supports JPG, PNG, and SVG files up to 10MB"}
              </p>
            </div>
            <label htmlFor="file-upload">
              <input id="file-upload" type="file" className="sr-only" accept="image/*" onChange={handleFileChange} />
              <Button
                variant="outline"
                size="lg"
                className="mt-2"
                onClick={() => document.getElementById("file-upload")?.click()}
              >
                Browse Files
              </Button>
            </label>
          </div>
        </CardContent>
      </Card>
    </section>
  )
}
