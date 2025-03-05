'use client';
import { useState } from "react";
import { 
  Card, CardContent, CardHeader, CardTitle 
} from "@/components/ui/card";
import { Tabs } from "@/components/ui/tabs";

export default function DeckPage() {
  const [problem, setProblem] = useState("");

  return (
    <div className="space-y-6 p-6 bg-white">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Quotation Recommender</h1>
      </div>

      <Tabs defaultValue="problem" className="w-full">
        <Card>
          <CardHeader>
         
          </CardHeader>
          <CardContent>
          <iframe
  width="100%"
  height="900px"
  className="rounded-md border"
  srcDoc={`
    <html>
      <body style='margin:0;padding:0;border:0;'>
        <iframe
          src='http://localhost:8501'
          width='100%'
          height='100%'
          style='border: none; display: block; width: 100vw; height: 100vh;'
          allow="microphone"
        ></iframe>
      </body>
    </html>
  `}
/>
          </CardContent>
        </Card>
      </Tabs>
    </div>
  );
}