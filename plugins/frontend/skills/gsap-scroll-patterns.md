---
skill: gsap-scroll-patterns
version: "1.0.0"
description: "Production-ready GSAP ScrollTrigger patterns for scroll-driven animations, parallax effects, and cinematic web experiences"
used-by:
  - "@animation-engineer"
  - "@layout-builder"
  - "@react-engineer"
  - "@frontend-controller"
---

# GSAP Scroll Patterns

## Overview

This skill covers production-ready patterns for scroll-driven animations using GSAP ScrollTrigger. Includes reveal animations, scrubbing, pinning, horizontal scroll, parallax effects, and performance optimization.

## 1. Setup and Installation

### Package Installation

```bash
npm install gsap @gsap/react
```

### Plugin Registration (Required)

```typescript
// lib/gsap.ts
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ScrollSmoother } from "gsap/ScrollSmoother";
import { SplitText } from "gsap/SplitText";

// Register plugins ONCE at app initialization
if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger, ScrollSmoother, SplitText);
}

export { gsap, ScrollTrigger, ScrollSmoother, SplitText };
```

### useGSAP Hook (React Integration)

```typescript
// hooks/useScrollAnimation.ts
import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

interface ScrollAnimationConfig {
  trigger?: string;
  start?: string;
  end?: string;
  scrub?: boolean | number;
  pin?: boolean;
  markers?: boolean;
}

export function useScrollAnimation(
  animationCallback: (context: gsap.Context) => void,
  config?: ScrollAnimationConfig
) {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const ctx = gsap.context(() => {
        animationCallback(gsap.context(() => {}));
      }, containerRef);

      return () => ctx.revert();
    },
    { scope: containerRef, dependencies: [] }
  );

  return containerRef;
}
```

### App-Level Setup (Next.js)

```typescript
// app/providers.tsx
"use client";

import { useEffect } from "react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

export function GSAPProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Configure GSAP defaults
    gsap.defaults({
      ease: "power3.out",
      duration: 0.8,
    });

    // Handle reduced motion preference
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReducedMotion) {
      gsap.globalTimeline.timeScale(20);
    }

    // Refresh ScrollTrigger after fonts/images load
    const refreshTriggers = () => ScrollTrigger.refresh();
    window.addEventListener("load", refreshTriggers);

    return () => {
      window.removeEventListener("load", refreshTriggers);
      ScrollTrigger.killAll();
    };
  }, []);

  return <>{children}</>;
}
```

---

## 2. ScrollTrigger Configurations

### Basic Reveal Animation

```typescript
// components/ScrollReveal.tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

interface ScrollRevealProps {
  children: React.ReactNode;
  direction?: "up" | "down" | "left" | "right";
  delay?: number;
  className?: string;
}

export function ScrollReveal({
  children,
  direction = "up",
  delay = 0,
  className,
}: ScrollRevealProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  const directionMap = {
    up: { y: 60, x: 0 },
    down: { y: -60, x: 0 },
    left: { y: 0, x: 60 },
    right: { y: 0, x: -60 },
  };

  useGSAP(
    () => {
      const { x, y } = directionMap[direction];

      gsap.from(containerRef.current, {
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top 85%",
          end: "top 50%",
          toggleActions: "play none none reverse",
        },
        x,
        y,
        opacity: 0,
        duration: 0.8,
        delay,
        ease: "power3.out",
      });
    },
    { scope: containerRef }
  );

  return (
    <div ref={containerRef} className={className}>
      {children}
    </div>
  );
}
```

### Scrub Animation (Progress-Based)

```typescript
// components/ScrubProgress.tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

export function ScrubProgress() {
  const containerRef = useRef<HTMLDivElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      // Timeline scrubbed to scroll position
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top top",
          end: "bottom bottom",
          scrub: 0.5, // Smoothing factor (0 = instant, 1+ = smoother)
        },
      });

      tl.to(progressRef.current, {
        scaleX: 1,
        ease: "none", // Linear for progress bars
      });
    },
    { scope: containerRef }
  );

  return (
    <div ref={containerRef} className="relative min-h-[200vh]">
      <div className="sticky top-0 h-1 w-full bg-gray-200">
        <div
          ref={progressRef}
          className="h-full w-full origin-left scale-x-0 bg-blue-500"
        />
      </div>
    </div>
  );
}
```

### Pin Section

```typescript
// components/PinnedSection.tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

interface PinnedSectionProps {
  children: React.ReactNode;
  duration?: number; // In viewport heights
}

export function PinnedSection({ children, duration = 2 }: PinnedSectionProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      ScrollTrigger.create({
        trigger: containerRef.current,
        start: "top top",
        end: `+=${window.innerHeight * duration}`,
        pin: contentRef.current,
        pinSpacing: true,
        anticipatePin: 1, // Prevents jitter
      });
    },
    { scope: containerRef }
  );

  return (
    <section ref={containerRef}>
      <div ref={contentRef} className="min-h-screen">
        {children}
      </div>
    </section>
  );
}
```

### Horizontal Scroll Section

```typescript
// components/HorizontalScroll.tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

interface HorizontalScrollProps {
  children: React.ReactNode;
  className?: string;
}

export function HorizontalScroll({
  children,
  className,
}: HorizontalScrollProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const trackRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const track = trackRef.current;
      if (!track) return;

      const scrollWidth = track.scrollWidth - window.innerWidth;

      gsap.to(track, {
        x: -scrollWidth,
        ease: "none",
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top top",
          end: () => `+=${scrollWidth}`,
          scrub: 1,
          pin: true,
          anticipatePin: 1,
          invalidateOnRefresh: true, // Recalculate on resize
        },
      });
    },
    { scope: containerRef }
  );

  return (
    <section ref={containerRef} className={className}>
      <div ref={trackRef} className="flex h-screen items-center">
        {children}
      </div>
    </section>
  );
}

// Usage
function PortfolioGallery() {
  return (
    <HorizontalScroll>
      {projects.map((project) => (
        <div key={project.id} className="h-[80vh] w-[80vw] flex-shrink-0 px-8">
          <ProjectCard project={project} />
        </div>
      ))}
    </HorizontalScroll>
  );
}
```

### toggleActions Reference

```typescript
// toggleActions format: "onEnter onLeave onEnterBack onLeaveBack"
// Values: "play", "pause", "resume", "reset", "restart", "complete", "reverse", "none"

const toggleActionsExamples = {
  // Play once, never reverse
  playOnce: "play none none none",

  // Play forward when entering, reverse when leaving
  playReverse: "play none none reverse",

  // Restart animation each time section enters
  restart: "restart none none none",

  // Full bidirectional
  fullBidirectional: "play reverse play reverse",

  // Complete immediately on enter, reset on leave
  instant: "complete none none reset",
};
```

---

## 3. Animation Patterns

### Stagger Reveal (Grid/List)

```typescript
// components/StaggerGrid.tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

interface StaggerGridProps {
  children: React.ReactNode;
  columns?: number;
  staggerFrom?: "start" | "end" | "center" | "edges" | "random";
}

export function StaggerGrid({
  children,
  columns = 3,
  staggerFrom = "start",
}: StaggerGridProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const items = containerRef.current?.querySelectorAll(".grid-item");
      if (!items?.length) return;

      gsap.from(items, {
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top 80%",
          toggleActions: "play none none reverse",
        },
        y: 60,
        opacity: 0,
        duration: 0.6,
        stagger: {
          each: 0.1,
          from: staggerFrom,
          grid: "auto",
          ease: "power2.out",
        },
      });
    },
    { scope: containerRef }
  );

  return (
    <div
      ref={containerRef}
      className="grid gap-6"
      style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}
    >
      {children}
    </div>
  );
}

// Usage
<StaggerGrid columns={3} staggerFrom="center">
  {items.map((item) => (
    <div key={item.id} className="grid-item">
      <Card {...item} />
    </div>
  ))}
</StaggerGrid>;
```

### Text Split Animation

```typescript
// components/SplitTextReveal.tsx
"use client";

import { useRef, useEffect, useState } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger, SplitText } from "@/lib/gsap";

interface SplitTextRevealProps {
  children: string;
  type?: "chars" | "words" | "lines";
  stagger?: number;
  className?: string;
}

export function SplitTextReveal({
  children,
  type = "chars",
  stagger = 0.02,
  className,
}: SplitTextRevealProps) {
  const textRef = useRef<HTMLDivElement>(null);
  const [isReady, setIsReady] = useState(false);

  useGSAP(
    () => {
      if (!textRef.current) return;

      // Split the text
      const split = new SplitText(textRef.current, {
        type: type,
        linesClass: "split-line",
        wordsClass: "split-word",
        charsClass: "split-char",
      });

      // Get the split elements
      const elements =
        type === "chars"
          ? split.chars
          : type === "words"
            ? split.words
            : split.lines;

      gsap.from(elements, {
        scrollTrigger: {
          trigger: textRef.current,
          start: "top 85%",
          toggleActions: "play none none reverse",
        },
        y: type === "lines" ? "100%" : 20,
        opacity: type === "lines" ? 1 : 0,
        duration: 0.6,
        stagger: stagger,
        ease: "power3.out",
        onComplete: () => setIsReady(true),
      });

      return () => split.revert();
    },
    { scope: textRef }
  );

  return (
    <div ref={textRef} className={className}>
      {children}
    </div>
  );
}

// Line-by-line reveal with mask
export function LineReveal({
  children,
  className,
}: {
  children: string;
  className?: string;
}) {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      if (!containerRef.current) return;

      const split = new SplitText(containerRef.current, {
        type: "lines",
        linesClass: "overflow-hidden",
      });

      // Wrap each line content for mask reveal
      split.lines.forEach((line) => {
        const wrapper = document.createElement("div");
        wrapper.innerHTML = line.innerHTML;
        line.innerHTML = "";
        line.appendChild(wrapper);
      });

      const lineContents = containerRef.current.querySelectorAll(
        ".overflow-hidden > div"
      );

      gsap.from(lineContents, {
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top 80%",
          toggleActions: "play none none reverse",
        },
        yPercent: 100,
        duration: 0.8,
        stagger: 0.1,
        ease: "power3.out",
      });

      return () => split.revert();
    },
    { scope: containerRef }
  );

  return (
    <div ref={containerRef} className={className}>
      {children}
    </div>
  );
}
```

### Parallax Effects

```typescript
// components/Parallax.tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

interface ParallaxProps {
  children: React.ReactNode;
  speed?: number; // Positive = slower, Negative = faster
  className?: string;
}

export function Parallax({ children, speed = 0.5, className }: ParallaxProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const yDistance = 100 * speed;

      gsap.fromTo(
        contentRef.current,
        { y: -yDistance },
        {
          y: yDistance,
          ease: "none",
          scrollTrigger: {
            trigger: containerRef.current,
            start: "top bottom",
            end: "bottom top",
            scrub: true,
          },
        }
      );
    },
    { scope: containerRef }
  );

  return (
    <div ref={containerRef} className={`overflow-hidden ${className}`}>
      <div ref={contentRef}>{children}</div>
    </div>
  );
}

// Parallax Image with scale effect
export function ParallaxImage({
  src,
  alt,
  speed = 0.3,
  scale = 1.2,
  className,
}: {
  src: string;
  alt: string;
  speed?: number;
  scale?: number;
  className?: string;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  useGSAP(
    () => {
      const yDistance = 50 * speed;

      gsap.fromTo(
        imageRef.current,
        {
          y: -yDistance,
          scale: scale,
        },
        {
          y: yDistance,
          scale: scale,
          ease: "none",
          scrollTrigger: {
            trigger: containerRef.current,
            start: "top bottom",
            end: "bottom top",
            scrub: true,
          },
        }
      );
    },
    { scope: containerRef }
  );

  return (
    <div ref={containerRef} className={`overflow-hidden ${className}`}>
      <img
        ref={imageRef}
        src={src}
        alt={alt}
        className="h-full w-full object-cover"
      />
    </div>
  );
}
```

### Progress-Based Animation

```typescript
// components/ScrollProgress.tsx
"use client";

import { useRef, useState } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

export function ScrollProgressSection() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [progress, setProgress] = useState(0);

  useGSAP(
    () => {
      ScrollTrigger.create({
        trigger: containerRef.current,
        start: "top top",
        end: "bottom bottom",
        onUpdate: (self) => {
          setProgress(Math.round(self.progress * 100));
        },
      });
    },
    { scope: containerRef }
  );

  return (
    <section ref={containerRef} className="min-h-[300vh]">
      <div className="sticky top-1/2 text-center">
        <span className="text-8xl font-bold">{progress}%</span>
      </div>
    </section>
  );
}

// Multi-step progress animation
export function SteppedProgress({ steps }: { steps: string[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [activeStep, setActiveStep] = useState(0);

  useGSAP(
    () => {
      const stepHeight = 100 / steps.length;

      ScrollTrigger.create({
        trigger: containerRef.current,
        start: "top top",
        end: "bottom bottom",
        onUpdate: (self) => {
          const currentStep = Math.min(
            Math.floor(self.progress * steps.length),
            steps.length - 1
          );
          setActiveStep(currentStep);
        },
      });
    },
    { scope: containerRef }
  );

  return (
    <section ref={containerRef} style={{ height: `${steps.length * 100}vh` }}>
      <div className="sticky top-0 flex h-screen items-center justify-center">
        <div className="space-y-4">
          {steps.map((step, index) => (
            <div
              key={index}
              className={`transition-all duration-300 ${
                index === activeStep
                  ? "scale-110 opacity-100"
                  : index < activeStep
                    ? "opacity-50"
                    : "opacity-20"
              }`}
            >
              {step}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

---

## 4. ScrollSmoother Integration

### Basic ScrollSmoother Setup

```typescript
// components/SmoothScrollProvider.tsx
"use client";

import { useRef, useEffect } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger, ScrollSmoother } from "@/lib/gsap";

interface SmoothScrollProviderProps {
  children: React.ReactNode;
  smooth?: number;
  effects?: boolean;
}

export function SmoothScrollProvider({
  children,
  smooth = 1,
  effects = true,
}: SmoothScrollProviderProps) {
  const wrapperRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReducedMotion) return;

    const smoother = ScrollSmoother.create({
      wrapper: wrapperRef.current,
      content: contentRef.current,
      smooth: smooth,
      effects: effects,
      smoothTouch: 0.1, // Light smoothing on touch devices
      normalizeScroll: true, // Prevents address bar issues on mobile
    });

    return () => smoother.kill();
  });

  return (
    <div ref={wrapperRef} id="smooth-wrapper">
      <div ref={contentRef} id="smooth-content">
        {children}
      </div>
    </div>
  );
}
```

### ScrollSmoother Effects

```typescript
// components/SmoothEffects.tsx
"use client";

// Speed effect - element scrolls slower/faster than page
export function SlowScroll({
  children,
  speed = 0.5,
}: {
  children: React.ReactNode;
  speed?: number;
}) {
  return <div data-speed={speed}>{children}</div>;
}

// Lag effect - element follows scroll with delay
export function LagScroll({
  children,
  lag = 0.5,
}: {
  children: React.ReactNode;
  lag?: number;
}) {
  return <div data-lag={lag}>{children}</div>;
}

// Combined effects example
export function HeroWithEffects() {
  return (
    <section className="relative h-screen">
      {/* Background moves slower */}
      <div data-speed="0.5" className="absolute inset-0">
        <img
          src="/hero-bg.jpg"
          alt=""
          className="h-full w-full object-cover"
        />
      </div>

      {/* Content has slight lag for depth */}
      <div data-lag="0.2" className="relative z-10 flex h-full items-center">
        <h1 className="text-6xl font-bold">Welcome</h1>
      </div>

      {/* Foreground element moves faster */}
      <div data-speed="1.5" className="absolute bottom-0 right-0">
        <FloatingElement />
      </div>
    </section>
  );
}
```

### ScrollSmoother with ScrollTrigger

```typescript
// Accessing ScrollSmoother in ScrollTrigger callbacks
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger, ScrollSmoother } from "@/lib/gsap";

export function SmoothScrollToSection() {
  const handleClick = (targetId: string) => {
    const smoother = ScrollSmoother.get();
    if (smoother) {
      smoother.scrollTo(`#${targetId}`, true, "top top");
    } else {
      // Fallback for when ScrollSmoother is not active
      document.getElementById(targetId)?.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <nav>
      <button onClick={() => handleClick("features")}>Features</button>
      <button onClick={() => handleClick("pricing")}>Pricing</button>
    </nav>
  );
}

// ScrollTrigger with smooth scroll offset
export function SmoothPinnedSection() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const smoother = ScrollSmoother.get();

      ScrollTrigger.create({
        trigger: containerRef.current,
        start: "top top",
        end: "+=200%",
        pin: true,
        // Use smoother's scroll position for accuracy
        scroller: smoother ? smoother.wrapper : undefined,
      });
    },
    { scope: containerRef }
  );

  return <section ref={containerRef}>...</section>;
}
```

---

## 5. Performance Optimization

### ScrollTrigger.batch for Large Lists

```typescript
// components/BatchReveal.tsx
"use client";

import { useRef, useEffect } from "react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

export function BatchReveal({ children }: { children: React.ReactNode }) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const items = containerRef.current?.querySelectorAll(".batch-item");
    if (!items?.length) return;

    // Batch processes multiple elements efficiently
    ScrollTrigger.batch(items, {
      onEnter: (batch) => {
        gsap.to(batch, {
          opacity: 1,
          y: 0,
          stagger: 0.1,
          duration: 0.6,
          ease: "power3.out",
        });
      },
      onLeave: (batch) => {
        gsap.to(batch, {
          opacity: 0,
          y: -20,
          stagger: 0.05,
        });
      },
      onEnterBack: (batch) => {
        gsap.to(batch, {
          opacity: 1,
          y: 0,
          stagger: 0.1,
        });
      },
      onLeaveBack: (batch) => {
        gsap.to(batch, {
          opacity: 0,
          y: 20,
          stagger: 0.05,
        });
      },
      start: "top 90%",
      end: "bottom 10%",
    });

    return () => ScrollTrigger.killAll();
  }, []);

  return (
    <div ref={containerRef}>
      {/* Items should have initial state */}
      <style jsx>{`
        .batch-item {
          opacity: 0;
          transform: translateY(40px);
        }
      `}</style>
      {children}
    </div>
  );
}
```

### Proper Cleanup Patterns

```typescript
// hooks/useCleanupScrollTrigger.ts
"use client";

import { useEffect, useRef } from "react";
import { gsap, ScrollTrigger } from "@/lib/gsap";

export function useCleanupScrollTrigger() {
  const triggersRef = useRef<ScrollTrigger[]>([]);

  useEffect(() => {
    return () => {
      // Kill all triggers created in this component
      triggersRef.current.forEach((trigger) => trigger.kill());
      triggersRef.current = [];
    };
  }, []);

  const createTrigger = (config: ScrollTrigger.Vars): ScrollTrigger => {
    const trigger = ScrollTrigger.create(config);
    triggersRef.current.push(trigger);
    return trigger;
  };

  return { createTrigger };
}

// Full cleanup example component
export function AnimatedSection() {
  const containerRef = useRef<HTMLDivElement>(null);
  const ctxRef = useRef<gsap.Context | null>(null);

  useEffect(() => {
    // Create GSAP context for automatic cleanup
    ctxRef.current = gsap.context(() => {
      gsap.from(".animated-element", {
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top 80%",
        },
        y: 50,
        opacity: 0,
      });
    }, containerRef);

    return () => {
      // Revert all animations in context
      ctxRef.current?.revert();
    };
  }, []);

  return <section ref={containerRef}>...</section>;
}
```

### Refresh Strategies

```typescript
// utils/scrollTriggerRefresh.ts
import { ScrollTrigger } from "@/lib/gsap";

// Refresh after dynamic content loads
export function refreshAfterImages(container: HTMLElement) {
  const images = container.querySelectorAll("img");
  let loadedCount = 0;

  images.forEach((img) => {
    if (img.complete) {
      loadedCount++;
    } else {
      img.addEventListener("load", () => {
        loadedCount++;
        if (loadedCount === images.length) {
          ScrollTrigger.refresh();
        }
      });
    }
  });

  if (loadedCount === images.length) {
    ScrollTrigger.refresh();
  }
}

// Refresh after fonts load
export function refreshAfterFonts() {
  if (document.fonts) {
    document.fonts.ready.then(() => {
      ScrollTrigger.refresh();
    });
  }
}

// Debounced refresh for resize
export function setupResizeRefresh() {
  let resizeTimeout: NodeJS.Timeout;

  const handleResize = () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      ScrollTrigger.refresh();
    }, 200);
  };

  window.addEventListener("resize", handleResize);

  return () => {
    window.removeEventListener("resize", handleResize);
    clearTimeout(resizeTimeout);
  };
}

// Refresh after route change (Next.js)
// In your layout or page component:
import { usePathname } from "next/navigation";
import { useEffect } from "react";

export function useRouteChangeRefresh() {
  const pathname = usePathname();

  useEffect(() => {
    // Small delay to ensure DOM is updated
    const timeout = setTimeout(() => {
      ScrollTrigger.refresh();
    }, 100);

    return () => clearTimeout(timeout);
  }, [pathname]);
}
```

### Memory-Efficient Patterns

```typescript
// Lazy initialization for heavy animations
"use client";

import { useRef, useState, useEffect } from "react";
import { useInView } from "react-intersection-observer";
import { gsap, ScrollTrigger } from "@/lib/gsap";

export function LazyAnimation({ children }: { children: React.ReactNode }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const { ref: inViewRef, inView } = useInView({
    threshold: 0,
    triggerOnce: true,
    rootMargin: "200px", // Initialize slightly before visible
  });

  useEffect(() => {
    if (inView && !isInitialized && containerRef.current) {
      // Initialize heavy animation only when approaching viewport
      gsap.from(".heavy-animation", {
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top 80%",
        },
        // ... animation config
      });

      setIsInitialized(true);
    }
  }, [inView, isInitialized]);

  return (
    <div ref={inViewRef}>
      <div ref={containerRef}>{children}</div>
    </div>
  );
}
```

---

## 6. Common Pitfalls and Solutions

### Pitfall 1: Animations Not Triggering

```typescript
// PROBLEM: ScrollTrigger created before DOM is ready
// BAD
useEffect(() => {
  gsap.from(".element", {
    scrollTrigger: { trigger: ".container" },
    y: 50,
  });
}, []); // Element might not exist yet

// GOOD: Use useGSAP with scope
const containerRef = useRef(null);
useGSAP(
  () => {
    gsap.from(".element", {
      scrollTrigger: { trigger: containerRef.current },
      y: 50,
    });
  },
  { scope: containerRef }
);
```

### Pitfall 2: Pinning Causes Layout Shift

```typescript
// PROBLEM: Pin spacing not accounted for
// BAD
ScrollTrigger.create({
  trigger: ".section",
  pin: true,
  // Missing pinSpacing consideration
});

// GOOD: Use pinSpacing or account for it
ScrollTrigger.create({
  trigger: ".section",
  pin: true,
  pinSpacing: true, // Adds space after pinned section
  anticipatePin: 1, // Prevents jump when pin starts
});

// Alternative: Container-based pinning
<div className="pin-container" style={{ height: "200vh" }}>
  <div className="pin-content sticky top-0 h-screen">
    {/* Pinned content */}
  </div>
</div>
```

### Pitfall 3: Horizontal Scroll Jitter

```typescript
// PROBLEM: Width calculation issues
// BAD
gsap.to(track, {
  x: -track.scrollWidth, // Wrong: includes visible area
});

// GOOD: Subtract viewport width
gsap.to(track, {
  x: -(track.scrollWidth - window.innerWidth),
  scrollTrigger: {
    invalidateOnRefresh: true, // Recalculate on resize
  },
});
```

### Pitfall 4: Memory Leaks

```typescript
// PROBLEM: ScrollTriggers not cleaned up
// BAD
useEffect(() => {
  ScrollTrigger.create({ ... });
  // No cleanup!
}, []);

// GOOD: Always clean up
useEffect(() => {
  const trigger = ScrollTrigger.create({ ... });
  return () => trigger.kill();
}, []);

// BETTER: Use GSAP context
useEffect(() => {
  const ctx = gsap.context(() => {
    ScrollTrigger.create({ ... });
  }, containerRef);
  return () => ctx.revert(); // Kills all animations/triggers in context
}, []);
```

### Pitfall 5: Mobile Performance Issues

```typescript
// PROBLEM: Heavy animations on mobile
// BAD
gsap.to(".particles", {
  // Complex animation runs on all devices
});

// GOOD: Reduce complexity on mobile
const isMobile = window.innerWidth < 768;

gsap.to(".particles", {
  scrollTrigger: {
    trigger: ".section",
    scrub: isMobile ? false : 0.5, // Disable scrub on mobile
  },
  // Simpler animation on mobile
  y: isMobile ? 20 : 100,
  stagger: isMobile ? 0 : 0.1,
});
```

### Pitfall 6: Flash of Unstyled Content

```typescript
// PROBLEM: Elements visible before animation starts
// BAD: CSS transition conflicts
.element {
  opacity: 0;
  transition: opacity 0.3s; // This fights GSAP
}

// GOOD: Set initial state in GSAP, hide with CSS initially
.element {
  visibility: hidden; // Prevent flash
}

// In GSAP
gsap.set(".element", { visibility: "visible", opacity: 0, y: 50 });
gsap.to(".element", {
  scrollTrigger: { trigger: ".container", start: "top 80%" },
  opacity: 1,
  y: 0
});
```

### Pitfall 7: Refresh Timing Issues

```typescript
// PROBLEM: Refresh called before layout settles
// BAD
useEffect(() => {
  ScrollTrigger.refresh(); // Too early!
}, [data]);

// GOOD: Wait for next frame
useEffect(() => {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      ScrollTrigger.refresh();
    });
  });
}, [data]);

// BETTER: Use GSAP's built-in delay
useEffect(() => {
  ScrollTrigger.refresh(true); // Safe refresh with recalculation
}, [data]);
```

---

## 7. Decision Matrix

### When to Use Each Approach

| Scenario | Recommended Approach | Why |
|----------|---------------------|-----|
| Simple reveal on scroll | `toggleActions: "play none none reverse"` | Lightweight, reversible |
| Progress indicator | `scrub: true` + linear ease | Direct scroll-to-progress mapping |
| Sticky section with content changes | `pin: true` + timeline | Full control over pinned duration |
| Horizontal gallery | Pin container + `x` tween | Smooth horizontal scroll experience |
| Parallax background | `scrub: true` + `fromTo` | Predictable start/end positions |
| Large list animation | `ScrollTrigger.batch()` | Performance optimized for many items |
| Text character animation | SplitText + stagger | Professional text reveals |
| Smooth page scroll | ScrollSmoother | Butter-smooth scrolling |
| Mobile-first project | CSS scroll-snap or simple reveals | Better performance |

### Scrub Value Guide

| Value | Behavior | Use Case |
|-------|----------|----------|
| `false` | No scrubbing (trigger-based) | Simple reveals |
| `true` or `0` | Instant scrub | Tight scroll-animation sync |
| `0.5 - 1` | Smooth scrub | Most scroll animations |
| `2 - 3` | Laggy scrub | Dreamy, delayed effects |

### Start/End Position Reference

```typescript
// Format: "trigger-position viewport-position"

const startEndExamples = {
  // Element top hits viewport 80% from top
  standardReveal: { start: "top 80%", end: "top 20%" },

  // Element top hits viewport top (pin starts)
  pinStart: { start: "top top", end: "+=100%" },

  // Element center hits viewport center
  centered: { start: "center center", end: "center center" },

  // Element bottom hits viewport bottom
  exitAnimation: { start: "bottom bottom", end: "top top" },

  // Pixel offsets
  withOffset: { start: "top top+=100", end: "bottom bottom-=50" },

  // Percentage of element
  percentBased: { start: "25% center", end: "75% center" },
};
```

### Performance Priority Matrix

| Priority | Technique | Impact |
|----------|-----------|--------|
| Critical | GPU properties only (transform, opacity) | 60fps animations |
| High | Batch processing for lists | Reduced ScrollTrigger instances |
| High | Proper cleanup on unmount | Prevents memory leaks |
| Medium | Lazy initialization | Faster initial load |
| Medium | Debounced refresh | Smoother resizing |
| Low | ScrollSmoother | Enhanced feel (optional) |

---

## 8. Complete Example: Cinematic Landing Page

```typescript
// components/CinematicLanding.tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap, ScrollTrigger, SplitText } from "@/lib/gsap";

export function CinematicLanding() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      // Hero entrance
      const heroTl = gsap.timeline();
      const heroSplit = new SplitText(".hero-title", { type: "chars" });

      heroTl
        .from(heroSplit.chars, {
          opacity: 0,
          y: 100,
          rotateX: -90,
          stagger: 0.02,
          duration: 1,
          ease: "back.out(1.7)",
        })
        .from(
          ".hero-subtitle",
          {
            opacity: 0,
            y: 30,
            duration: 0.8,
          },
          "-=0.5"
        )
        .from(
          ".hero-cta",
          {
            opacity: 0,
            scale: 0.8,
            duration: 0.5,
          },
          "-=0.3"
        );

      // Parallax hero background
      gsap.to(".hero-bg", {
        y: 200,
        ease: "none",
        scrollTrigger: {
          trigger: ".hero",
          start: "top top",
          end: "bottom top",
          scrub: true,
        },
      });

      // Features section - staggered cards
      gsap.from(".feature-card", {
        scrollTrigger: {
          trigger: ".features",
          start: "top 70%",
          toggleActions: "play none none reverse",
        },
        y: 100,
        opacity: 0,
        duration: 0.8,
        stagger: {
          each: 0.15,
          from: "start",
        },
      });

      // Stats counter - pinned with scrub
      const statsTl = gsap.timeline({
        scrollTrigger: {
          trigger: ".stats",
          start: "top top",
          end: "+=150%",
          pin: true,
          scrub: 1,
        },
      });

      statsTl
        .from(".stat-number", {
          textContent: 0,
          duration: 1,
          snap: { textContent: 1 },
          stagger: 0.2,
        })
        .from(
          ".stat-label",
          {
            opacity: 0,
            y: 20,
            stagger: 0.1,
          },
          "-=0.5"
        );

      // Testimonial horizontal scroll
      const testimonialTrack = document.querySelector(".testimonial-track");
      if (testimonialTrack) {
        const scrollWidth =
          testimonialTrack.scrollWidth - window.innerWidth + 100;

        gsap.to(".testimonial-track", {
          x: -scrollWidth,
          ease: "none",
          scrollTrigger: {
            trigger: ".testimonials",
            start: "top top",
            end: () => `+=${scrollWidth}`,
            pin: true,
            scrub: 1,
            anticipatePin: 1,
          },
        });
      }

      // CTA section - scale reveal
      gsap.from(".final-cta", {
        scrollTrigger: {
          trigger: ".final-cta",
          start: "top 80%",
          end: "top 30%",
          scrub: true,
        },
        scale: 0.8,
        opacity: 0,
        borderRadius: "50%",
      });

      // Cleanup
      return () => {
        heroSplit.revert();
      };
    },
    { scope: containerRef }
  );

  return (
    <div ref={containerRef}>
      {/* Hero */}
      <section className="hero relative h-screen overflow-hidden">
        <div className="hero-bg absolute inset-0">
          <img
            src="/hero-bg.jpg"
            alt=""
            className="h-full w-full object-cover"
          />
        </div>
        <div className="relative z-10 flex h-full flex-col items-center justify-center">
          <h1 className="hero-title text-7xl font-bold">Welcome</h1>
          <p className="hero-subtitle mt-4 text-xl">Your journey starts here</p>
          <button className="hero-cta mt-8 rounded-full bg-white px-8 py-4">
            Get Started
          </button>
        </div>
      </section>

      {/* Features */}
      <section className="features py-32">
        <div className="mx-auto grid max-w-6xl grid-cols-3 gap-8">
          {[1, 2, 3].map((i) => (
            <div key={i} className="feature-card rounded-xl bg-gray-100 p-8">
              Feature {i}
            </div>
          ))}
        </div>
      </section>

      {/* Stats */}
      <section className="stats flex h-screen items-center justify-center bg-black text-white">
        <div className="grid grid-cols-3 gap-16 text-center">
          {[
            { number: 100, label: "Projects" },
            { number: 50, label: "Clients" },
            { number: 10, label: "Years" },
          ].map((stat, i) => (
            <div key={i}>
              <div className="stat-number text-6xl font-bold">{stat.number}</div>
              <div className="stat-label mt-2">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Testimonials */}
      <section className="testimonials h-screen overflow-hidden">
        <div className="testimonial-track flex h-full items-center gap-8 px-8">
          {[1, 2, 3, 4, 5].map((i) => (
            <div
              key={i}
              className="h-[60vh] w-[80vw] flex-shrink-0 rounded-2xl bg-gray-100 p-12"
            >
              Testimonial {i}
            </div>
          ))}
        </div>
      </section>

      {/* Final CTA */}
      <section className="final-cta flex h-screen items-center justify-center bg-blue-600 text-white">
        <div className="text-center">
          <h2 className="text-5xl font-bold">Ready to Start?</h2>
          <button className="mt-8 rounded-full bg-white px-8 py-4 text-blue-600">
            Contact Us
          </button>
        </div>
      </section>
    </div>
  );
}
```

---

## Quick Reference

### Essential Imports

```typescript
import gsap from "gsap";
import { useGSAP } from "@gsap/react";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ScrollSmoother } from "gsap/ScrollSmoother";
import { SplitText } from "gsap/SplitText";

gsap.registerPlugin(ScrollTrigger, ScrollSmoother, SplitText);
```

### Common Configurations

```typescript
// Reveal animation
{ start: "top 80%", toggleActions: "play none none reverse" }

// Scrub animation
{ start: "top bottom", end: "bottom top", scrub: 0.5 }

// Pin section
{ start: "top top", end: "+=100%", pin: true, anticipatePin: 1 }

// Horizontal scroll
{ start: "top top", end: () => `+=${scrollWidth}`, pin: true, scrub: 1 }
```

### Reduced Motion Support

```typescript
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches;

if (prefersReducedMotion) {
  gsap.globalTimeline.timeScale(20);
  // Or disable animations entirely
  ScrollTrigger.config({ autoRefreshEvents: "visibilitychange,DOMContentLoaded,load" });
}
```
