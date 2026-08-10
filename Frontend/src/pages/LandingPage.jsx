// src/pages/LandingPage.jsx
import 'react';
import HeroSection from '../components/landing/HeroSection';
import ExploreSection from '../components/landing/ExploreSection';
import TravelFeatureSection from '../components/landing/TravelFeatureSection';
import WhyChooseUs from '../components/landing/WhyChooseUs';
import DestinationSection from '../components/landing/DestinationSection';
import Footer from '../components/landing/Footer';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <main className="flex-1">
        <HeroSection />
        <ExploreSection />
        <TravelFeatureSection />
        <WhyChooseUs />
        <DestinationSection />
      </main>
      <Footer />
    </div>
  );
}