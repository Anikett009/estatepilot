"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search } from "lucide-react";
import React from "react";
import { DotLottieReact } from "@lottiefiles/dotlottie-react";

export default function MatchPage() {
  const [city, setCity] = useState("");
  const [properties, setProperties] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchProperties = async () => {
    setLoading(true);
    setError("");
    setProperties([]);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/properties?city=${encodeURIComponent(city)}`,
        {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        }
      );

      if (!response.ok) throw new Error("Failed to fetch properties");

      const data = await response.json();

      if (!Array.isArray(data)) {
        throw new Error("Invalid response format");
      }

      const filteredProperties = data.map((property) => ({
        name: property.title || "Unnamed Property",
        type: property.property_type || "Unknown Type",
        price: property.price_range || "Price not available",
        location: property.location?.address || "Location not available",
        builder: property.builder || "Unknown Builder",
        possessionStatus: property.possession_status || "Status not available",
        coverImage: property.cover_image || "",
        coordinates: property.location?.coordinates || ["0", "0"], // Default if missing
        configurations:
          property.configurations?.map((config) => ({
            type: config.type || "Unknown Type",
            carpetArea: config.carpet_area || "N/A",
            price: config.price || "N/A",
          })) || [],
      }));

      setProperties(filteredProperties);
    } catch (err) {
      setError("Error fetching properties");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Property Listings</h1>
      </div>

      <div className="flex gap-x-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Enter a city name"
            className="pl-9"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
        </div>
        <Button onClick={fetchProperties} disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </Button>
      </div>

      {error && <p className="text-red-500">{error}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {properties.length > 0 ? (
          properties.map((property, index) => (
            <Card key={index} className="p-4 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  {/* Lottie Animation + Property Name */}
                  <div className="flex items-center gap-2">
                    <DotLottieReact
                      src="https://lottie.host/89fd9ebc-7140-407b-aa40-b75a040e3409/L8d2GbCtbz.lottie"
                      loop
                      autoplay
                      className="w-50 h-50"
                    />
                    <span className="text-lg font-semibold">{property.name}</span>
                  </div>
                  <Badge>{property.type}</Badge>
                </CardTitle>
              </CardHeader>

              <CardContent className="space-y-2">
                <p className="text-sm text-gray-700">Price: {property.price}</p>
                <p className="text-sm text-gray-700">Location: {property.location}</p>
                <p className="text-sm text-gray-700">Builder: {property.builder}</p>
                <p className="text-sm text-gray-700">Possession Status: {property.possessionStatus}</p>

                {/* Display Coordinates */}
                <p className="text-sm text-gray-700">
                  Coordinates: {property.coordinates[0]}, {property.coordinates[1]}
                </p>

                {/* Google Maps Redirect Button */}
                <Button
                  className="bg-green-500 text-white w-full mt-2"
                  onClick={() =>
                    window.open(
                      `https://www.google.com/maps?q=${property.coordinates[0]},${property.coordinates[1]}`,
                      "_blank"
                    )
                  }
                >
                  View on Google Maps
                </Button>

                {property.configurations.length > 0 && (
                  <div className="mt-2">
                    <p className="text-sm font-semibold">Configurations:</p>
                    {property.configurations.map((config, idx) => (
                      <p key={idx} className="text-xs text-gray-500">
                        {config.type}: {config.carpetArea} sq.ft - {config.price}
                      </p>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))
        ) : (
          <p className="text-gray-500">No properties found</p>
        )}
      </div>
    </div>
  );
}
