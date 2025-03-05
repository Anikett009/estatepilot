"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function DocumentProcessor() {
  const [file, setFile] = useState<File | null>(null);
  const [language, setLanguage] = useState("en");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please upload a file.");
      return;
    }
    setLoading(true);
    setError("");
    setOutput("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("target_language", language);

    try {
      console.log("Uploading file:", file.name);
      console.log("Target language:", language);

      const response = await fetch("http://127.0.0.1:5003/process", {
        method: "POST",
        body: formData,
      });

      console.log("Response status:", response.status);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to process document: ${errorText}`);
      }

      const data = await response.json();
      console.log("Response data:", data);
      setOutput(data.summary);
    } catch (err: any) {
      console.error("Error:", err);
      setError(err.message || "Error processing the document.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Legal Document Summarizer</h1>

      <Card className="bg-white p-6 shadow-md rounded">
        <CardHeader>
          <CardTitle>Upload a legal document (PDF or DOCX)</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-4">
            <Label htmlFor="file">Select File</Label>
            <Input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
          </div>

          <div className="mb-4">
            <Label htmlFor="target_language">Select Target Language</Label>
            <select
              id="target_language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="mt-2 p-2 border rounded w-full"
            >
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="mr">Marathi</option>
              <option value="te">Telugu</option>
            </select>
          </div>

          <Button onClick={handleSubmit} disabled={loading} className="w-full bg-blue-500 text-white">
            {loading ? "Processing..." : "Summarize"}
          </Button>

          {error && <p className="text-red-500 mt-4">{error}</p>}
        </CardContent>
      </Card>

      {output && (
        <Card className="mt-6 bg-white p-6 shadow-md rounded">
          <CardHeader>
            <CardTitle>Processed Output</CardTitle>
          </CardHeader>
          <CardContent>
            <textarea value={output} readOnly className="w-full h-40 p-2 border rounded" />
          </CardContent>
        </Card>
      )}
    </div>
  );
}
