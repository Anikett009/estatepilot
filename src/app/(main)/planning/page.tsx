"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Download, TrendingUp, BarChart, FileText, Map } from "lucide-react";

// Define TypeScript types for structured API response
interface RevenueProjection {
  period: string;
  revenue: string;
  growth: string;
}

interface ExpenseBreakdown {
  category: string;
  amount: string;
  percentage: string;
}

interface FinancialPlan {
  roadmap: string[];
  revenueProjections: RevenueProjection[];
  expenseBreakdown: ExpenseBreakdown[];
  requiredDocuments: string[];
}

export default function FinancialPlanningPage() {
  const [businessDetails, setBusinessDetails] = useState({
    businessName: "",
    industry: "",
    startupCost: "",
    revenueStreams: "",
    operatingExpenses: "",
    fundingSources: "",
  });

  const [plan, setPlan] = useState<FinancialPlan | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setBusinessDetails((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch("/api/finance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(businessDetails),
      });

      if (!response.ok) {
        throw new Error("Failed to generate financial plan.");
      }

      const data: FinancialPlan = await response.json();
      console.log("API Response:", data); // Debugging Step
      setPlan(data);
    } catch (error) {
      console.error("Error fetching plan:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-3xl font-bold">Financial Planning</h1>

      {/* Form Input Section */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Business Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Label>Business Name</Label>
            <Input name="businessName" value={businessDetails.businessName} onChange={handleInputChange} required />

            <Label>Industry</Label>
            <Input name="industry" value={businessDetails.industry} onChange={handleInputChange} required />

            <Label>Estimated Startup Cost</Label>
            <Input name="startupCost" value={businessDetails.startupCost} onChange={handleInputChange} required />

            <Label>Revenue Streams</Label>
            <Input name="revenueStreams" value={businessDetails.revenueStreams} onChange={handleInputChange} required />

            <Label>Operating Expenses</Label>
            <Input name="operatingExpenses" value={businessDetails.operatingExpenses} onChange={handleInputChange} required />

            <Label>Funding Sources</Label>
            <Input name="fundingSources" value={businessDetails.fundingSources} onChange={handleInputChange} required />

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? "Generating Plan..." : "Generate Financial Plan"}
            </Button>
          </CardContent>
        </Card>
      </form>

      {/* Financial Plan Display Section */}
      {plan && (
        <div className="space-y-6">
          {/* Business Roadmap */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-x-2">
                <Map className="h-5 w-5 text-purple-600" />
                Business Roadmap
              </CardTitle>
            </CardHeader>
            <CardContent>
              {plan.roadmap && plan.roadmap.length > 0 ? (
                <ol className="list-decimal pl-5">
                  {plan.roadmap.map((step, index) => (
                    <li key={index}>{step}</li>
                  ))}
                </ol>
              ) : (
                <p>No roadmap provided.</p>
              )}
            </CardContent>
          </Card>

          {/* Revenue Projections */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-x-2">
                <TrendingUp className="h-5 w-5 text-green-600" />
                Revenue Projections
              </CardTitle>
            </CardHeader>
            <CardContent>
              {plan.revenueProjections && plan.revenueProjections.length > 0 ? (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Period</TableHead>
                      <TableHead>Revenue</TableHead>
                      <TableHead>Growth</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {plan.revenueProjections.map((item, index) => (
                      <TableRow key={index}>
                        <TableCell>{item.period}</TableCell>
                        <TableCell>{item.revenue}</TableCell>
                        <TableCell>{item.growth}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <p>No revenue projections available.</p>
              )}
            </CardContent>
          </Card>

          {/* Expense Breakdown */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-x-2">
                <BarChart className="h-5 w-5 text-blue-600" />
                Expense Breakdown
              </CardTitle>
            </CardHeader>
            <CardContent>
              {plan.expenseBreakdown && plan.expenseBreakdown.length > 0 ? (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Category</TableHead>
                      <TableHead>Amount</TableHead>
                      <TableHead>% of Total</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {plan.expenseBreakdown.map((expense, index) => (
                      <TableRow key={index}>
                        <TableCell>{expense.category}</TableCell>
                        <TableCell>{expense.amount}</TableCell>
                        <TableCell>{expense.percentage}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <p>No expense breakdown available.</p>
              )}
            </CardContent>
          </Card>

          {/* Required Documents */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-x-2">
                <FileText className="h-5 w-5 text-gray-600" />
                Required Documents
              </CardTitle>
            </CardHeader>
            <CardContent>
              {plan.requiredDocuments && plan.requiredDocuments.length > 0 ? (
                <ul className="list-disc pl-5">
                  {plan.requiredDocuments.map((doc, index) => (
                    <li key={index}>{doc}</li>
                  ))}
                </ul>
              ) : (
                <p>No documents required.</p>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
