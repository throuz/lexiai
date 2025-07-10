import LexiAIClient from "../components/LexiAIClient";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 gap-8 bg-gray-50 dark:bg-black">
      <h1 className="text-3xl font-bold mb-2">LexiAI 法律文件摘要與問答</h1>
      <LexiAIClient />
    </div>
  );
}
