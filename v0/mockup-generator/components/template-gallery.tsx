"use client"

import { useState } from "react"
import { Check } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"

interface Template {
  id: string
  name: string
  image: string
  category: string
}

export function TemplateGallery() {
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null)

  const templates: Template[] = [
    { id: "1", name: "MacBook Pro", image: "/placeholder.svg?height=200&width=300", category: "Laptop" },
    { id: "2", name: "iPhone 15", image: "/placeholder.svg?height=200&width=300", category: "Mobile" },
    { id: "3", name: "iPad Pro", image: "/placeholder.svg?height=200&width=300", category: "Tablet" },
    { id: "4", name: "Desktop Monitor", image: "/placeholder.svg?height=200&width=300", category: "Desktop" },
    { id: "5", name: "Billboard", image: "/placeholder.svg?height=200&width=300", category: "Outdoor" },
    { id: "6", name: "Business Card", image: "/placeholder.svg?height=200&width=300", category: "Print" },
  ]

  return (
    <section className="w-full space-y-4">
      <div className="flex flex-col space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Choose a Template</h2>
        <p className="text-muted-foreground">Select a mockup template for your design</p>
      </div>

      <ScrollArea className="w-full whitespace-nowrap pb-6">
        <div className="flex w-max space-x-4 p-1">
          {templates.map((template) => (
            <Card
              key={template.id}
              className={`w-[250px] cursor-pointer transition-all hover:shadow-md ${
                selectedTemplate === template.id ? "ring-2 ring-primary" : ""
              }`}
              onClick={() => setSelectedTemplate(template.id)}
            >
              <CardContent className="p-0">
                <div className="relative">
                  <img
                    src={template.image || "/placeholder.svg"}
                    alt={template.name}
                    className="h-[150px] w-full object-cover"
                  />
                  {selectedTemplate === template.id && (
                    <div className="absolute right-2 top-2 rounded-full bg-primary p-1">
                      <Check className="h-4 w-4 text-primary-foreground" />
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="font-medium">{template.name}</h3>
                  <p className="text-xs text-muted-foreground">{template.category}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </section>
  )
}
