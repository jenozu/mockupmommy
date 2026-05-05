"use client"

import { useState } from "react"
import { Download, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export function PreviewSection() {
  const [isLoading, setIsLoading] = useState(false)
  const [isGenerated, setIsGenerated] = useState(false)

  const handleGenerate = () => {
    setIsLoading(true)
    // Simulate processing time
    setTimeout(() => {
      setIsLoading(false)
      setIsGenerated(true)
    }, 3000)
  }

  return (
    <section className="w-full space-y-6">
      <div className="flex flex-col space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Preview Your Mockup</h2>
        <p className="text-muted-foreground">Generate and download your professional mockup</p>
      </div>

      <Card className="overflow-hidden">
        <CardContent className="p-0">
          <Tabs defaultValue="preview" className="w-full">
            <div className="flex items-center justify-between border-b px-4">
              <TabsList className="h-14">
                <TabsTrigger value="preview">Preview</TabsTrigger>
                <TabsTrigger value="before-after">Before & After</TabsTrigger>
              </TabsList>
              <div className="flex items-center gap-2">
                {!isGenerated ? (
                  <Button onClick={handleGenerate} disabled={isLoading} className="gap-2">
                    {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
                    {isLoading ? "Processing..." : "Generate Mockup"}
                  </Button>
                ) : (
                  <Button className="gap-2">
                    <Download className="h-4 w-4" />
                    Download
                  </Button>
                )}
              </div>
            </div>

            <TabsContent value="preview" className="m-0">
              <div className="flex h-[500px] items-center justify-center bg-muted/30">
                {isLoading ? (
                  <div className="flex flex-col items-center justify-center space-y-4 text-center">
                    <Loader2 className="h-10 w-10 animate-spin text-muted-foreground" />
                    <div>
                      <p className="font-medium">Processing your mockup</p>
                      <p className="text-sm text-muted-foreground">This may take a few moments...</p>
                    </div>
                  </div>
                ) : isGenerated ? (
                  <img
                    src="/placeholder.svg?height=450&width=800"
                    alt="Generated Mockup"
                    className="max-h-[450px] w-auto object-contain"
                  />
                ) : (
                  <div className="text-center">
                    <p className="text-muted-foreground">
                      Upload an image and select a template to generate your mockup
                    </p>
                  </div>
                )}
              </div>
            </TabsContent>

            <TabsContent value="before-after" className="m-0">
              <div className="grid h-[500px] grid-cols-2 gap-4 bg-muted/30 p-6">
                <div className="flex flex-col items-center justify-center space-y-2 rounded-lg border border-dashed p-4">
                  <p className="font-medium">Original Design</p>
                  {isGenerated ? (
                    <img
                      src="/placeholder.svg?height=300&width=300"
                      alt="Original Design"
                      className="max-h-[300px] w-auto object-contain"
                    />
                  ) : (
                    <p className="text-sm text-muted-foreground">No image uploaded</p>
                  )}
                </div>
                <div className="flex flex-col items-center justify-center space-y-2 rounded-lg border border-dashed p-4">
                  <p className="font-medium">Mockup Result</p>
                  {isGenerated ? (
                    <img
                      src="/placeholder.svg?height=300&width=300"
                      alt="Mockup Result"
                      className="max-h-[300px] w-auto object-contain"
                    />
                  ) : (
                    <p className="text-sm text-muted-foreground">No mockup generated</p>
                  )}
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </section>
  )
}
