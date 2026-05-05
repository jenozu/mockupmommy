import { HeroSection } from "@/components/hero-section"
import { UploadArea } from "@/components/upload-area"
import { TemplateGallery } from "@/components/template-gallery"
import { PreviewSection } from "@/components/preview-section"

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-background to-muted/20">
      <HeroSection />
      <div className="container px-4 py-12 mx-auto space-y-16 md:py-16 lg:py-24">
        <UploadArea />
        <TemplateGallery />
        <PreviewSection />
      </div>
    </main>
  )
}
