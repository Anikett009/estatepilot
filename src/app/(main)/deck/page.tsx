'use client';
import { useState } from "react";
import { 
  Card, CardContent, CardHeader, CardTitle 
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Target, Download } from "lucide-react";

export default function DeckPage() {
  const [problem, setProblem] = useState("");

  return (
    <div className="space-y-6 p-6 bg-white">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Conversations</h1>
      </div>

      <Tabs defaultValue="problem" className="w-full">
          <Card>
            <CardHeader>
              <CardTitle>Chat with fellow users</CardTitle>
            </CardHeader>
            <CardContent>
              <iframe
                src="http://localhost:8503"
                width="100%"
                height="900px"
                className="rounded-md border"
              />
            </CardContent>
          </Card>

      </Tabs>
    </div>
  );
}
