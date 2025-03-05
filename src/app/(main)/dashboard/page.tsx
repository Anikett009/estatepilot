import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight, BarChart2, BookOpen, Users, Wallet } from "lucide-react";
import Link from "next/link";

export default function LearnPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Welcome to EstatePilot</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-x-2">
              <BarChart2 className="h-5 w-5 text-green-600" />
              Real Estate Chatbot
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Analyze your conversations with other users to collect important details
            </p>
            <Button asChild>
              <Link href="/validation" className="flex items-center gap-x-2">
                Talk With Chatbot <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-x-2">
              <BarChart2 className="h-5 w-5 text-green-600" />
              Multilingual Conversations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Talk with other users in multiple languages
            </p>
            <Button asChild>
              <Link href="/elevatorpitch" className="flex items-center gap-x-2">
                Start Chatting <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-x-2">
              <BookOpen className="h-5 w-5 text-blue-600" />
              Property Listing
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Get properties related to your query
            </p>
            <Button asChild>
              <Link href="/deck" className="flex items-center gap-x-2">
                Enter Query <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-x-2">
              <Wallet className="h-5 w-5 text-purple-600" />
              Follow Up
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Record and Schedule meetings with estate agents in any language 
            </p>
            <Button asChild>
              <Link href="/planning" className="flex items-center gap-x-2">
                Start Recording <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-x-2">
              <Users className="h-5 w-5 text-orange-600" />
              Multilingual Summarizer
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Summarize files in any language
            </p>
            <Button asChild>
              <Link href="/match" className="flex items-center gap-x-2">
                Summarize <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-x-2">
              <BarChart2 className="h-5 w-5 text-green-600" />
              Real Estate Recommender
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
          Receive top real estate properties based on user preferences and feedback.
            </p>
            <Button asChild>
              <Link href="/automation" className="flex items-center gap-x-2">
                Chat  <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-x-2">
              <BookOpen className="h-5 w-5 text-green-600" />
              Ad Generator
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Generate multilingual ads based on prompt
            </p>
            <Button asChild>
              <Link href="/automation" className="flex items-center gap-x-2">
                Generate  <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}