"use client";
import { useRef, useState } from "react";

export default function LexiAIClient() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [pdfText, setPdfText] = useState("");
  const [summary, setSummary] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [uploading, setUploading] = useState(false);
  const [summarizing, setSummarizing] = useState(false);
  const [qaLoading, setQaLoading] = useState(false);
  const [fileId, setFileId] = useState<number | null>(null);
  const [error, setError] = useState("");

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "";

  // PDF 上傳
  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    setError("");
    setSummary("");
    setAnswer("");
    setUploading(true);
    const files = e.target.files;
    if (!files || files.length === 0) return;
    const file = files[0];
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setPdfText(data.text);
      setFileId(data.id);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setUploading(false);
    }
  };

  // 摘要
  const handleSummarize = async () => {
    setError("");
    setSummarizing(true);
    setSummary("");
    try {
      const res = await fetch(`${API_BASE}/summarize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: pdfText, id: fileId }),
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setSummary(data.summary);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSummarizing(false);
    }
  };

  // 問答
  const handleQA = async () => {
    setError("");
    setQaLoading(true);
    setAnswer("");
    try {
      const res = await fetch(`${API_BASE}/qa`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: pdfText, question }),
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setAnswer(data.answer);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setQaLoading(false);
    }
  };

  // 狀態重置
  const handleReset = () => {
    setPdfText("");
    setSummary("");
    setQuestion("");
    setAnswer("");
    setFileId(null);
    setError("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="w-full max-w-xl bg-white dark:bg-gray-900 rounded-lg shadow p-6 flex flex-col gap-6">
      <div className="flex justify-end mb-2">
        <button
          className="text-xs px-3 py-1 rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200"
          onClick={handleReset}
        >
          重新開始
        </button>
      </div>
      <label className="block">
        <span className="font-medium">上傳法律 PDF</span>
        <input
          type="file"
          accept="application/pdf"
          ref={fileInputRef}
          onChange={handleUpload}
          className="block mt-2"
          disabled={uploading || !!pdfText}
        />
      </label>
      {uploading && <div className="text-blue-500">上傳中...</div>}
      {pdfText && (
        <>
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
            onClick={handleSummarize}
            disabled={summarizing}
          >
            {summarizing ? "摘要生成中..." : "產生摘要"}
          </button>
          <div>
            <span className="font-medium">原文擷取：</span>
            <pre className="bg-gray-100 dark:bg-gray-800 p-2 rounded max-h-40 overflow-auto text-xs whitespace-pre-wrap">
              {pdfText}
            </pre>
          </div>
        </>
      )}
      {summary && (
        <div>
          <span className="font-medium">AI 摘要：</span>
          <pre className="bg-blue-50 dark:bg-blue-900 p-2 rounded max-h-40 overflow-auto text-sm whitespace-pre-wrap">
            {summary}
          </pre>
        </div>
      )}
      {pdfText && (
        <div className="flex flex-col gap-2">
          <label className="font-medium">問答</label>
          <input
            type="text"
            className="border rounded px-2 py-1"
            placeholder="請輸入你的問題..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={qaLoading}
          />
          <button
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
            onClick={handleQA}
            disabled={qaLoading || !question}
          >
            {qaLoading ? "AI 回答中..." : "送出問題"}
          </button>
          {answer && (
            <div>
              <span className="font-medium">AI 回答：</span>
              <pre className="bg-green-50 dark:bg-green-900 p-2 rounded max-h-40 overflow-auto text-sm whitespace-pre-wrap">
                {answer}
              </pre>
            </div>
          )}
        </div>
      )}
      {error && <div className="text-red-500">{error}</div>}
    </div>
  );
}
