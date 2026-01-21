---
skill: framer-motion-variants
version: 1.0.0
used-by:
  - animation-engineer
  - interaction-designer
---

# Framer Motion Variants and Animation Patterns

Comprehensive guide to building production-ready animations with Framer Motion in React and Next.js applications.

## 1. Core Concepts

### Motion Components

The `motion` component is the foundation of Framer Motion. Any HTML or SVG element can be animated by prefixing it with `motion.`.

```tsx
import { motion } from "framer-motion";

// Basic animated div
export function AnimatedBox() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className="p-6 bg-white rounded-lg shadow-lg"
    >
      Content fades and slides in
    </motion.div>
  );
}
```

### Variants System

Variants allow you to define animation states as objects and reference them by name. This enables orchestrated animations across component trees.

```tsx
import { motion, type Variants } from "framer-motion";

const cardVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 50,
    scale: 0.95,
  },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      duration: 0.5,
      ease: "easeOut",
    },
  },
  hover: {
    scale: 1.02,
    boxShadow: "0 20px 40px rgba(0,0,0,0.15)",
    transition: {
      duration: 0.2,
    },
  },
  tap: {
    scale: 0.98,
  },
};

export function Card({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      whileHover="hover"
      whileTap="tap"
      className="p-6 bg-white rounded-xl"
    >
      {children}
    </motion.div>
  );
}
```

### AnimatePresence

`AnimatePresence` enables exit animations for components that are removed from the React tree.

```tsx
"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";

interface Notification {
  id: string;
  message: string;
}

const notificationVariants: Variants = {
  initial: { opacity: 0, x: 100, scale: 0.9 },
  animate: { opacity: 1, x: 0, scale: 1 },
  exit: { opacity: 0, x: 100, scale: 0.9 },
};

export function NotificationStack() {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = (message: string) => {
    const id = crypto.randomUUID();
    setNotifications((prev) => [...prev, { id, message }]);

    // Auto-dismiss after 3 seconds
    setTimeout(() => {
      setNotifications((prev) => prev.filter((n) => n.id !== id));
    }, 3000);
  };

  const removeNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
      <AnimatePresence mode="popLayout">
        {notifications.map((notification) => (
          <motion.div
            key={notification.id}
            variants={notificationVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            layout
            className="p-4 bg-white rounded-lg shadow-lg min-w-[300px]"
          >
            <div className="flex items-center justify-between">
              <p>{notification.message}</p>
              <button
                onClick={() => removeNotification(notification.id)}
                className="ml-4 text-gray-500 hover:text-gray-700"
              >
                Dismiss
              </button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>

      <button
        onClick={() => addNotification("New notification")}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
      >
        Add Notification
      </button>
    </div>
  );
}
```

---

## 2. Reusable Variant Library

Create a centralized variants file for consistent animations across your application.

```tsx
// lib/animation-variants.ts
import type { Variants, Transition } from "framer-motion";

// ============================================
// TRANSITION PRESETS
// ============================================

export const transitions = {
  spring: {
    type: "spring",
    stiffness: 300,
    damping: 30,
  } as Transition,

  springBouncy: {
    type: "spring",
    stiffness: 400,
    damping: 17,
  } as Transition,

  springGentle: {
    type: "spring",
    stiffness: 120,
    damping: 20,
  } as Transition,

  easeOut: {
    duration: 0.3,
    ease: [0.25, 0.46, 0.45, 0.94],
  } as Transition,

  easeInOut: {
    duration: 0.4,
    ease: [0.65, 0, 0.35, 1],
  } as Transition,
} as const;

// ============================================
// FADE VARIANTS
// ============================================

export const fadeVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: transitions.easeOut,
  },
  exit: { opacity: 0 },
};

export const fadeUpVariants: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: transitions.easeOut,
  },
  exit: { opacity: 0, y: 24 },
};

export const fadeDownVariants: Variants = {
  hidden: { opacity: 0, y: -24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: transitions.easeOut,
  },
  exit: { opacity: 0, y: -24 },
};

// ============================================
// SLIDE VARIANTS
// ============================================

export const slideLeftVariants: Variants = {
  hidden: { x: "-100%", opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    transition: transitions.spring,
  },
  exit: { x: "-100%", opacity: 0 },
};

export const slideRightVariants: Variants = {
  hidden: { x: "100%", opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    transition: transitions.spring,
  },
  exit: { x: "100%", opacity: 0 },
};

export const slideUpVariants: Variants = {
  hidden: { y: "100%", opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: transitions.spring,
  },
  exit: { y: "100%", opacity: 0 },
};

// ============================================
// SCALE VARIANTS
// ============================================

export const scaleVariants: Variants = {
  hidden: { scale: 0.8, opacity: 0 },
  visible: {
    scale: 1,
    opacity: 1,
    transition: transitions.springBouncy,
  },
  exit: { scale: 0.8, opacity: 0 },
};

export const scaleUpVariants: Variants = {
  hidden: { scale: 0, opacity: 0 },
  visible: {
    scale: 1,
    opacity: 1,
    transition: transitions.springBouncy,
  },
  exit: { scale: 0, opacity: 0 },
};

export const popVariants: Variants = {
  hidden: { scale: 0.5, opacity: 0 },
  visible: {
    scale: 1,
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 500,
      damping: 25,
    },
  },
  exit: { scale: 0.5, opacity: 0 },
};

// ============================================
// STAGGER VARIANTS
// ============================================

export const staggerContainerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1,
    },
  },
  exit: {
    opacity: 0,
    transition: {
      staggerChildren: 0.05,
      staggerDirection: -1,
    },
  },
};

export const staggerItemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: transitions.spring,
  },
  exit: { opacity: 0, y: 20 },
};

// Factory function for custom stagger timing
export function createStaggerVariants(
  staggerDelay: number = 0.1,
  delayChildren: number = 0
): { container: Variants; item: Variants } {
  return {
    container: {
      hidden: { opacity: 0 },
      visible: {
        opacity: 1,
        transition: {
          staggerChildren: staggerDelay,
          delayChildren,
        },
      },
    },
    item: {
      hidden: { opacity: 0, y: 20 },
      visible: {
        opacity: 1,
        y: 0,
        transition: transitions.spring,
      },
    },
  };
}

// ============================================
// MODAL VARIANTS
// ============================================

export const modalOverlayVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.2 },
  },
  exit: {
    opacity: 0,
    transition: { duration: 0.2, delay: 0.1 },
  },
};

export const modalContentVariants: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.95,
    y: 20,
  },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 25,
    },
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    y: 20,
    transition: { duration: 0.15 },
  },
};

export const drawerVariants: Variants = {
  hidden: { x: "100%" },
  visible: {
    x: 0,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 30,
    },
  },
  exit: {
    x: "100%",
    transition: { duration: 0.2 },
  },
};

// ============================================
// ACCORDION VARIANTS
// ============================================

export const accordionVariants: Variants = {
  collapsed: {
    height: 0,
    opacity: 0,
    transition: {
      height: { duration: 0.3 },
      opacity: { duration: 0.2 },
    },
  },
  expanded: {
    height: "auto",
    opacity: 1,
    transition: {
      height: { duration: 0.3 },
      opacity: { duration: 0.3, delay: 0.1 },
    },
  },
};

export const accordionIconVariants: Variants = {
  collapsed: { rotate: 0 },
  expanded: { rotate: 180 },
};

// ============================================
// CARD VARIANTS
// ============================================

export const cardVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 30,
    scale: 0.96,
  },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: transitions.spring,
  },
  hover: {
    y: -4,
    scale: 1.02,
    boxShadow: "0 20px 40px -12px rgba(0,0,0,0.2)",
    transition: { duration: 0.2 },
  },
  tap: {
    scale: 0.98,
  },
};

// ============================================
// BUTTON VARIANTS
// ============================================

export const buttonVariants: Variants = {
  idle: { scale: 1 },
  hover: { scale: 1.05 },
  tap: { scale: 0.95 },
};

export const buttonLoadingVariants: Variants = {
  idle: { opacity: 1 },
  loading: {
    opacity: [1, 0.5, 1],
    transition: {
      duration: 1.5,
      repeat: Infinity,
    },
  },
};
```

### Using the Variant Library

```tsx
// components/AnimatedList.tsx
"use client";

import { motion } from "framer-motion";
import {
  staggerContainerVariants,
  staggerItemVariants,
  cardVariants,
} from "@/lib/animation-variants";

interface Item {
  id: string;
  title: string;
  description: string;
}

export function AnimatedList({ items }: { items: Item[] }) {
  return (
    <motion.ul
      variants={staggerContainerVariants}
      initial="hidden"
      animate="visible"
      className="grid gap-4 md:grid-cols-2 lg:grid-cols-3"
    >
      {items.map((item) => (
        <motion.li
          key={item.id}
          variants={staggerItemVariants}
        >
          <motion.article
            variants={cardVariants}
            initial="hidden"
            animate="visible"
            whileHover="hover"
            whileTap="tap"
            className="p-6 bg-white rounded-xl shadow-sm"
          >
            <h3 className="text-lg font-semibold">{item.title}</h3>
            <p className="mt-2 text-gray-600">{item.description}</p>
          </motion.article>
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

---

## 3. Scroll Animations

### whileInView

Trigger animations when elements enter the viewport.

```tsx
"use client";

import { motion, type Variants } from "framer-motion";

const revealVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 75,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5,
      ease: "easeOut",
    },
  },
};

export function ScrollRevealSection() {
  return (
    <motion.section
      variants={revealVariants}
      initial="hidden"
      whileInView="visible"
      viewport={{
        once: true,    // Only animate once
        margin: "-100px", // Trigger 100px before entering viewport
        amount: 0.3,   // Trigger when 30% visible
      }}
      className="py-24"
    >
      <h2 className="text-4xl font-bold">Revealed on scroll</h2>
      <p className="mt-4 text-gray-600">
        This section animates when it enters the viewport.
      </p>
    </motion.section>
  );
}

// Staggered scroll reveal for multiple items
export function StaggeredScrollReveal({ items }: { items: string[] }) {
  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
      },
    },
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 40 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
  };

  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-50px" }}
      className="space-y-4"
    >
      {items.map((item, index) => (
        <motion.li
          key={index}
          variants={itemVariants}
          className="p-4 bg-white rounded-lg shadow"
        >
          {item}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### useScroll and useTransform

Create scroll-linked animations with fine-grained control.

```tsx
"use client";

import { motion, useScroll, useTransform, useSpring } from "framer-motion";
import { useRef } from "react";

// Parallax hero section
export function ParallaxHero() {
  const ref = useRef<HTMLElement>(null);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });

  // Transform scroll progress to animation values
  const y = useTransform(scrollYProgress, [0, 1], ["0%", "50%"]);
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [1, 0.5, 0]);
  const scale = useTransform(scrollYProgress, [0, 1], [1, 0.8]);

  return (
    <section ref={ref} className="relative h-screen overflow-hidden">
      <motion.div
        style={{ y, scale }}
        className="absolute inset-0"
      >
        <img
          src="/hero-bg.jpg"
          alt=""
          className="w-full h-full object-cover"
        />
      </motion.div>

      <motion.div
        style={{ opacity }}
        className="relative z-10 flex items-center justify-center h-full"
      >
        <h1 className="text-6xl font-bold text-white">
          Parallax Hero
        </h1>
      </motion.div>
    </section>
  );
}

// Scroll progress indicator
export function ScrollProgressBar() {
  const { scrollYProgress } = useScroll();

  // Add spring physics for smoother animation
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001,
  });

  return (
    <motion.div
      style={{ scaleX }}
      className="fixed top-0 left-0 right-0 h-1 bg-blue-600 origin-left z-50"
    />
  );
}

// Horizontal scroll section
export function HorizontalScroll({ items }: { items: React.ReactNode[] }) {
  const containerRef = useRef<HTMLDivElement>(null);

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"],
  });

  const x = useTransform(
    scrollYProgress,
    [0, 1],
    ["0%", `-${(items.length - 1) * 100}%`]
  );

  return (
    <div ref={containerRef} style={{ height: `${items.length * 100}vh` }}>
      <div className="sticky top-0 h-screen overflow-hidden">
        <motion.div
          style={{ x }}
          className="flex h-full"
        >
          {items.map((item, index) => (
            <div
              key={index}
              className="flex-shrink-0 w-screen h-full flex items-center justify-center"
            >
              {item}
            </div>
          ))}
        </motion.div>
      </div>
    </div>
  );
}

// Text reveal on scroll
export function ScrollTextReveal({ text }: { text: string }) {
  const ref = useRef<HTMLParagraphElement>(null);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start 0.9", "start 0.25"],
  });

  const words = text.split(" ");

  return (
    <p ref={ref} className="text-4xl font-bold leading-relaxed flex flex-wrap gap-2">
      {words.map((word, index) => {
        const start = index / words.length;
        const end = start + 1 / words.length;

        return (
          <Word
            key={index}
            progress={scrollYProgress}
            range={[start, end]}
          >
            {word}
          </Word>
        );
      })}
    </p>
  );
}

function Word({
  children,
  progress,
  range,
}: {
  children: string;
  progress: MotionValue<number>;
  range: [number, number];
}) {
  const opacity = useTransform(progress, range, [0.2, 1]);

  return (
    <motion.span style={{ opacity }}>
      {children}
    </motion.span>
  );
}
```

### Scroll-Triggered Number Counter

```tsx
"use client";

import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import { useEffect, useRef, useState } from "react";

interface CounterProps {
  from: number;
  to: number;
  duration?: number;
  suffix?: string;
  prefix?: string;
}

export function ScrollCounter({
  from,
  to,
  duration = 2,
  suffix = "",
  prefix = "",
}: CounterProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const [inView, setInView] = useState(false);
  const count = useMotionValue(from);
  const rounded = useTransform(count, (latest) => Math.round(latest));

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !inView) {
          setInView(true);
        }
      },
      { threshold: 0.5 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, [inView]);

  useEffect(() => {
    if (inView) {
      const animation = animate(count, to, {
        duration,
        ease: "easeOut",
      });
      return animation.stop;
    }
  }, [inView, count, to, duration]);

  return (
    <span ref={ref} className="tabular-nums">
      {prefix}
      <motion.span>{rounded}</motion.span>
      {suffix}
    </span>
  );
}

// Usage
export function StatsSection() {
  return (
    <section className="py-24 bg-gray-50">
      <div className="grid grid-cols-3 gap-8 max-w-4xl mx-auto text-center">
        <div>
          <p className="text-5xl font-bold">
            <ScrollCounter from={0} to={500} suffix="+" />
          </p>
          <p className="mt-2 text-gray-600">Projects Completed</p>
        </div>
        <div>
          <p className="text-5xl font-bold">
            <ScrollCounter from={0} to={98} suffix="%" />
          </p>
          <p className="mt-2 text-gray-600">Client Satisfaction</p>
        </div>
        <div>
          <p className="text-5xl font-bold">
            <ScrollCounter from={0} to={24} prefix="$" suffix="M" />
          </p>
          <p className="mt-2 text-gray-600">Revenue Generated</p>
        </div>
      </div>
    </section>
  );
}
```

---

## 4. Gesture Animations

### Hover, Tap, and Focus States

```tsx
"use client";

import { motion, type Variants } from "framer-motion";

// Interactive button with multiple states
const buttonVariants: Variants = {
  idle: {
    scale: 1,
    boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
  },
  hover: {
    scale: 1.05,
    boxShadow: "0 10px 20px -5px rgba(0, 0, 0, 0.2)",
  },
  tap: {
    scale: 0.95,
    boxShadow: "0 2px 4px -1px rgba(0, 0, 0, 0.1)",
  },
};

export function InteractiveButton({
  children,
  onClick,
}: {
  children: React.ReactNode;
  onClick?: () => void;
}) {
  return (
    <motion.button
      variants={buttonVariants}
      initial="idle"
      whileHover="hover"
      whileTap="tap"
      whileFocus="hover"
      onClick={onClick}
      className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
    >
      {children}
    </motion.button>
  );
}

// Card with hover reveal
const cardContainerVariants: Variants = {
  idle: {},
  hover: {},
};

const cardOverlayVariants: Variants = {
  idle: { opacity: 0 },
  hover: { opacity: 1 },
};

const cardContentVariants: Variants = {
  idle: { y: 20, opacity: 0 },
  hover: { y: 0, opacity: 1 },
};

export function HoverRevealCard({
  image,
  title,
  description,
}: {
  image: string;
  title: string;
  description: string;
}) {
  return (
    <motion.article
      variants={cardContainerVariants}
      initial="idle"
      whileHover="hover"
      className="relative overflow-hidden rounded-xl aspect-[4/5] cursor-pointer"
    >
      <img
        src={image}
        alt=""
        className="w-full h-full object-cover"
      />

      <motion.div
        variants={cardOverlayVariants}
        className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"
      />

      <motion.div
        variants={cardContentVariants}
        transition={{ duration: 0.3 }}
        className="absolute bottom-0 left-0 right-0 p-6 text-white"
      >
        <h3 className="text-xl font-bold">{title}</h3>
        <p className="mt-2 text-white/80">{description}</p>
      </motion.div>
    </motion.article>
  );
}

// Magnetic button effect
export function MagneticButton({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLButtonElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!ref.current) return;

    const rect = ref.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    const deltaX = (e.clientX - centerX) * 0.3;
    const deltaY = (e.clientY - centerY) * 0.3;

    setPosition({ x: deltaX, y: deltaY });
  };

  const handleMouseLeave = () => {
    setPosition({ x: 0, y: 0 });
  };

  return (
    <motion.button
      ref={ref}
      animate={{ x: position.x, y: position.y }}
      transition={{ type: "spring", stiffness: 150, damping: 15 }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      className="px-8 py-4 bg-black text-white rounded-full font-medium"
    >
      {children}
    </motion.button>
  );
}
```

### Drag Interactions

```tsx
"use client";

import { motion, useMotionValue, useTransform } from "framer-motion";

// Basic draggable card
export function DraggableCard() {
  return (
    <motion.div
      drag
      dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
      dragElastic={0.2}
      dragTransition={{ bounceStiffness: 600, bounceDamping: 20 }}
      whileDrag={{ scale: 1.05, cursor: "grabbing" }}
      className="w-48 h-48 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl shadow-xl cursor-grab"
    />
  );
}

// Swipe-to-delete item
export function SwipeableItem({
  children,
  onDelete,
}: {
  children: React.ReactNode;
  onDelete: () => void;
}) {
  const x = useMotionValue(0);
  const background = useTransform(
    x,
    [-200, 0],
    ["#ef4444", "#ffffff"]
  );
  const deleteOpacity = useTransform(x, [-200, -100, 0], [1, 0.5, 0]);

  const handleDragEnd = () => {
    if (x.get() < -150) {
      onDelete();
    }
  };

  return (
    <div className="relative overflow-hidden">
      <motion.div
        style={{ opacity: deleteOpacity }}
        className="absolute inset-y-0 right-0 flex items-center justify-end pr-4 bg-red-500 w-full"
      >
        <span className="text-white font-medium">Delete</span>
      </motion.div>

      <motion.div
        style={{ x, background }}
        drag="x"
        dragConstraints={{ left: -200, right: 0 }}
        dragElastic={{ left: 0.5, right: 0 }}
        onDragEnd={handleDragEnd}
        className="relative p-4 bg-white rounded-lg shadow cursor-grab active:cursor-grabbing"
      >
        {children}
      </motion.div>
    </div>
  );
}

// Drag to reorder list
import { Reorder } from "framer-motion";

interface Item {
  id: string;
  text: string;
}

export function ReorderableList() {
  const [items, setItems] = useState<Item[]>([
    { id: "1", text: "First item" },
    { id: "2", text: "Second item" },
    { id: "3", text: "Third item" },
  ]);

  return (
    <Reorder.Group
      axis="y"
      values={items}
      onReorder={setItems}
      className="space-y-2"
    >
      {items.map((item) => (
        <Reorder.Item
          key={item.id}
          value={item}
          className="p-4 bg-white rounded-lg shadow cursor-grab active:cursor-grabbing active:shadow-lg"
        >
          {item.text}
        </Reorder.Item>
      ))}
    </Reorder.Group>
  );
}
```

---

## 5. Layout Animations

### Basic Layout Animation

The `layout` prop enables automatic animation when a component's layout changes.

```tsx
"use client";

import { motion } from "framer-motion";
import { useState } from "react";

export function ExpandingCard() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <motion.div
      layout
      onClick={() => setIsExpanded(!isExpanded)}
      className={`
        bg-white rounded-xl shadow-lg cursor-pointer overflow-hidden
        ${isExpanded ? "p-8" : "p-4"}
      `}
      transition={{
        layout: { duration: 0.3, ease: "easeInOut" },
      }}
    >
      <motion.h3 layout="position" className="font-bold text-lg">
        Click to expand
      </motion.h3>

      {isExpanded && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.15 }}
          className="mt-4 text-gray-600"
        >
          Additional content that appears when expanded.
          The card animates smoothly to accommodate this content.
        </motion.p>
      )}
    </motion.div>
  );
}
```

### Shared Layout Animations with layoutId

The `layoutId` prop enables seamless transitions between components.

```tsx
"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";

interface Tab {
  id: string;
  label: string;
  content: React.ReactNode;
}

export function AnimatedTabs({ tabs }: { tabs: Tab[] }) {
  const [activeTab, setActiveTab] = useState(tabs[0].id);

  return (
    <div>
      <div className="flex gap-2 border-b">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`
              relative px-4 py-2 text-sm font-medium transition-colors
              ${activeTab === tab.id ? "text-blue-600" : "text-gray-600"}
            `}
          >
            {tab.label}
            {activeTab === tab.id && (
              <motion.div
                layoutId="activeTab"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600"
                transition={{ type: "spring", stiffness: 500, damping: 30 }}
              />
            )}
          </button>
        ))}
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
          className="py-6"
        >
          {tabs.find((t) => t.id === activeTab)?.content}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

// Card expand to modal
interface CardItem {
  id: string;
  title: string;
  image: string;
  description: string;
}

export function ExpandableCards({ items }: { items: CardItem[] }) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selectedItem = items.find((item) => item.id === selectedId);

  return (
    <>
      <div className="grid grid-cols-3 gap-4">
        {items.map((item) => (
          <motion.div
            key={item.id}
            layoutId={`card-${item.id}`}
            onClick={() => setSelectedId(item.id)}
            className="bg-white rounded-xl overflow-hidden shadow cursor-pointer"
          >
            <motion.img
              layoutId={`image-${item.id}`}
              src={item.image}
              alt=""
              className="w-full aspect-video object-cover"
            />
            <motion.div layoutId={`content-${item.id}`} className="p-4">
              <motion.h3 layoutId={`title-${item.id}`} className="font-bold">
                {item.title}
              </motion.h3>
            </motion.div>
          </motion.div>
        ))}
      </div>

      <AnimatePresence>
        {selectedId && selectedItem && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedId(null)}
              className="fixed inset-0 bg-black/50 z-40"
            />

            <motion.div
              layoutId={`card-${selectedId}`}
              className="fixed inset-4 md:inset-20 bg-white rounded-2xl overflow-hidden shadow-2xl z-50"
            >
              <button
                onClick={() => setSelectedId(null)}
                className="absolute top-4 right-4 z-10 p-2 bg-white/90 rounded-full"
              >
                Close
              </button>

              <motion.img
                layoutId={`image-${selectedId}`}
                src={selectedItem.image}
                alt=""
                className="w-full h-64 object-cover"
              />

              <motion.div layoutId={`content-${selectedId}`} className="p-8">
                <motion.h3
                  layoutId={`title-${selectedId}`}
                  className="text-2xl font-bold"
                >
                  {selectedItem.title}
                </motion.h3>
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  className="mt-4 text-gray-600"
                >
                  {selectedItem.description}
                </motion.p>
              </motion.div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
```

### LayoutGroup

Use `LayoutGroup` to scope layout animations and prevent conflicts.

```tsx
"use client";

import { LayoutGroup, motion } from "framer-motion";

export function FilterableGrid() {
  const [filter, setFilter] = useState("all");
  const items = [
    { id: 1, category: "design", title: "Design Project" },
    { id: 2, category: "dev", title: "Development" },
    { id: 3, category: "design", title: "Brand Identity" },
    { id: 4, category: "dev", title: "Web App" },
  ];

  const filteredItems =
    filter === "all"
      ? items
      : items.filter((item) => item.category === filter);

  return (
    <LayoutGroup>
      <div className="flex gap-2 mb-6">
        {["all", "design", "dev"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`
              relative px-4 py-2 rounded-full text-sm font-medium
              ${filter === f ? "text-white" : "text-gray-600"}
            `}
          >
            {filter === f && (
              <motion.div
                layoutId="filterBg"
                className="absolute inset-0 bg-blue-600 rounded-full -z-10"
              />
            )}
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <motion.div layout className="grid grid-cols-2 gap-4">
        {filteredItems.map((item) => (
          <motion.div
            key={item.id}
            layout
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="p-6 bg-white rounded-xl shadow"
          >
            {item.title}
          </motion.div>
        ))}
      </motion.div>
    </LayoutGroup>
  );
}
```

---

## 6. Spring Physics Configurations

### Understanding Spring Parameters

```tsx
// lib/spring-presets.ts
import type { Transition } from "framer-motion";

/**
 * Spring Physics Reference:
 *
 * - stiffness: How "tight" the spring is (higher = faster, more rigid)
 * - damping: How much resistance/friction (higher = less oscillation)
 * - mass: The "weight" of the object (higher = slower, more momentum)
 *
 * Relationship:
 * - High stiffness + low damping = bouncy
 * - High stiffness + high damping = snappy
 * - Low stiffness + low damping = floaty/slow
 * - Low stiffness + high damping = sluggish
 */

export const springPresets = {
  // Snappy - Quick response, minimal bounce
  // Good for: buttons, toggles, quick UI feedback
  snappy: {
    type: "spring",
    stiffness: 400,
    damping: 30,
    mass: 1,
  } as Transition,

  // Bouncy - Energetic with overshoot
  // Good for: notifications, celebrations, attention-grabbing
  bouncy: {
    type: "spring",
    stiffness: 400,
    damping: 15,
    mass: 1,
  } as Transition,

  // Gentle - Smooth and soft
  // Good for: modals, page transitions, large movements
  gentle: {
    type: "spring",
    stiffness: 120,
    damping: 20,
    mass: 1,
  } as Transition,

  // Heavy - Weighty feel with momentum
  // Good for: dragging, large elements, physical feel
  heavy: {
    type: "spring",
    stiffness: 200,
    damping: 30,
    mass: 2,
  } as Transition,

  // Wobbly - Playful bounce
  // Good for: fun interactions, gamification
  wobbly: {
    type: "spring",
    stiffness: 180,
    damping: 12,
    mass: 1,
  } as Transition,

  // Stiff - Very quick, almost no bounce
  // Good for: tooltips, fast micro-interactions
  stiff: {
    type: "spring",
    stiffness: 700,
    damping: 40,
    mass: 1,
  } as Transition,

  // Slow - Deliberate, cinematic
  // Good for: hero animations, dramatic reveals
  slow: {
    type: "spring",
    stiffness: 50,
    damping: 15,
    mass: 1,
  } as Transition,
} as const;

// Factory function for custom springs
export function createSpring(
  stiffness: number,
  damping: number,
  mass: number = 1
): Transition {
  return {
    type: "spring",
    stiffness,
    damping,
    mass,
  };
}
```

### Spring Visualization Component

```tsx
"use client";

import { motion, useSpring, useMotionValue } from "framer-motion";
import { useState } from "react";

interface SpringConfig {
  stiffness: number;
  damping: number;
  mass: number;
}

export function SpringPlayground() {
  const [config, setConfig] = useState<SpringConfig>({
    stiffness: 300,
    damping: 20,
    mass: 1,
  });

  const x = useMotionValue(0);
  const springX = useSpring(x, config);

  const triggerAnimation = () => {
    x.set(200);
    setTimeout(() => x.set(0), 100);
  };

  return (
    <div className="p-8 space-y-8">
      <div className="space-y-4">
        <label className="block">
          <span className="text-sm font-medium">Stiffness: {config.stiffness}</span>
          <input
            type="range"
            min="50"
            max="1000"
            value={config.stiffness}
            onChange={(e) =>
              setConfig({ ...config, stiffness: Number(e.target.value) })
            }
            className="w-full"
          />
        </label>

        <label className="block">
          <span className="text-sm font-medium">Damping: {config.damping}</span>
          <input
            type="range"
            min="1"
            max="100"
            value={config.damping}
            onChange={(e) =>
              setConfig({ ...config, damping: Number(e.target.value) })
            }
            className="w-full"
          />
        </label>

        <label className="block">
          <span className="text-sm font-medium">Mass: {config.mass}</span>
          <input
            type="range"
            min="0.1"
            max="5"
            step="0.1"
            value={config.mass}
            onChange={(e) =>
              setConfig({ ...config, mass: Number(e.target.value) })
            }
            className="w-full"
          />
        </label>
      </div>

      <div className="relative h-20 bg-gray-100 rounded-lg overflow-hidden">
        <motion.div
          style={{ x: springX }}
          className="absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 bg-blue-600 rounded-full"
        />
      </div>

      <button
        onClick={triggerAnimation}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg"
      >
        Trigger Animation
      </button>

      <pre className="p-4 bg-gray-900 text-gray-100 rounded-lg text-sm">
        {JSON.stringify(config, null, 2)}
      </pre>
    </div>
  );
}
```

---

## 7. Page Transitions with Next.js

### App Router Page Transitions

```tsx
// app/template.tsx
"use client";

import { motion } from "framer-motion";

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{
        type: "spring",
        stiffness: 260,
        damping: 20,
      }}
    >
      {children}
    </motion.div>
  );
}
```

### Full Page Transition System

```tsx
// components/page-transition/TransitionProvider.tsx
"use client";

import { AnimatePresence, motion, type Variants } from "framer-motion";
import { usePathname } from "next/navigation";
import { createContext, useContext, useState, type ReactNode } from "react";

type TransitionType = "fade" | "slide" | "scale" | "none";

interface TransitionContextValue {
  transitionType: TransitionType;
  setTransitionType: (type: TransitionType) => void;
}

const TransitionContext = createContext<TransitionContextValue | null>(null);

export function useTransition() {
  const context = useContext(TransitionContext);
  if (!context) {
    throw new Error("useTransition must be used within TransitionProvider");
  }
  return context;
}

const transitionVariants: Record<TransitionType, Variants> = {
  fade: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
  },
  slide: {
    initial: { opacity: 0, x: 100 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -100 },
  },
  scale: {
    initial: { opacity: 0, scale: 0.95 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 1.05 },
  },
  none: {
    initial: {},
    animate: {},
    exit: {},
  },
};

export function TransitionProvider({ children }: { children: ReactNode }) {
  const [transitionType, setTransitionType] = useState<TransitionType>("fade");
  const pathname = usePathname();

  return (
    <TransitionContext.Provider value={{ transitionType, setTransitionType }}>
      <AnimatePresence mode="wait">
        <motion.div
          key={pathname}
          variants={transitionVariants[transitionType]}
          initial="initial"
          animate="animate"
          exit="exit"
          transition={{ duration: 0.3 }}
        >
          {children}
        </motion.div>
      </AnimatePresence>
    </TransitionContext.Provider>
  );
}
```

### Cinematic Page Transitions

```tsx
// components/page-transition/CinematicTransition.tsx
"use client";

import { AnimatePresence, motion } from "framer-motion";
import { usePathname } from "next/navigation";
import { useState, useEffect, type ReactNode } from "react";

const overlayVariants = {
  initial: { scaleY: 0 },
  animate: {
    scaleY: 1,
    transition: {
      duration: 0.5,
      ease: [0.65, 0, 0.35, 1],
    },
  },
  exit: {
    scaleY: 0,
    transition: {
      duration: 0.5,
      ease: [0.65, 0, 0.35, 1],
      delay: 0.3,
    },
  },
};

const contentVariants = {
  initial: { opacity: 0 },
  animate: {
    opacity: 1,
    transition: {
      duration: 0.5,
      delay: 0.5,
    },
  },
  exit: {
    opacity: 0,
    transition: {
      duration: 0.3,
    },
  },
};

export function CinematicTransition({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    setIsAnimating(true);
    const timer = setTimeout(() => setIsAnimating(false), 1000);
    return () => clearTimeout(timer);
  }, [pathname]);

  return (
    <>
      <AnimatePresence>
        {isAnimating && (
          <motion.div
            variants={overlayVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            className="fixed inset-0 z-50 bg-black origin-bottom"
          />
        )}
      </AnimatePresence>

      <AnimatePresence mode="wait">
        <motion.div
          key={pathname}
          variants={contentVariants}
          initial="initial"
          animate="animate"
          exit="exit"
        >
          {children}
        </motion.div>
      </AnimatePresence>
    </>
  );
}
```

### Staggered Page Load Animation

```tsx
// components/page-transition/StaggeredPage.tsx
"use client";

import { motion, type Variants } from "framer-motion";
import { type ReactNode } from "react";

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 24,
    },
  },
};

interface StaggeredPageProps {
  children: ReactNode;
}

export function StaggeredPage({ children }: StaggeredPageProps) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {children}
    </motion.div>
  );
}

export function StaggeredItem({ children }: { children: ReactNode }) {
  return <motion.div variants={itemVariants}>{children}</motion.div>;
}

// Usage in page
export function ExamplePage() {
  return (
    <StaggeredPage>
      <StaggeredItem>
        <header className="py-8">
          <h1 className="text-4xl font-bold">Page Title</h1>
        </header>
      </StaggeredItem>

      <StaggeredItem>
        <section className="py-8">
          <p>First section content</p>
        </section>
      </StaggeredItem>

      <StaggeredItem>
        <section className="py-8">
          <p>Second section content</p>
        </section>
      </StaggeredItem>

      <StaggeredItem>
        <footer className="py-8">
          <p>Footer content</p>
        </footer>
      </StaggeredItem>
    </StaggeredPage>
  );
}
```

---

## 8. Performance and Accessibility

### Performance Best Practices

```tsx
// lib/animation-performance.ts

/**
 * Performance Guidelines for Framer Motion:
 *
 * 1. Use transform and opacity only when possible
 *    - These properties are GPU-accelerated
 *    - Avoid animating width, height, top, left, etc.
 *
 * 2. Use willChange for complex animations
 *    - Hints to browser about upcoming changes
 *    - Use sparingly to avoid memory overhead
 *
 * 3. Use layout="position" instead of layout when only position changes
 *    - Avoids expensive layout recalculations
 *
 * 4. Use AnimatePresence mode="popLayout" for better exit animations
 *    - Prevents layout jumps during exit
 *
 * 5. Prefer useTransform over manual calculations
 *    - Values are calculated outside React render cycle
 */

import { useReducedMotion } from "framer-motion";

// Hook to get motion-safe variants
export function useMotionSafeVariants<T extends object>(
  variants: T,
  reducedVariants?: Partial<T>
): T {
  const shouldReduceMotion = useReducedMotion();

  if (shouldReduceMotion && reducedVariants) {
    return { ...variants, ...reducedVariants };
  }

  return variants;
}
```

### Reduced Motion Support

```tsx
"use client";

import { motion, useReducedMotion, type Variants } from "framer-motion";

// Variants that respect reduced motion preference
const cardVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3 },
  },
};

const reducedMotionVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.1 },
  },
};

export function AccessibleCard({ children }: { children: React.ReactNode }) {
  const shouldReduceMotion = useReducedMotion();
  const variants = shouldReduceMotion ? reducedMotionVariants : cardVariants;

  return (
    <motion.div
      variants={variants}
      initial="hidden"
      animate="visible"
      className="p-6 bg-white rounded-xl shadow"
    >
      {children}
    </motion.div>
  );
}

// Higher-order component for reduced motion
export function withReducedMotion<P extends object>(
  Component: React.ComponentType<P>,
  staticProps?: Partial<P>
) {
  return function ReducedMotionWrapper(props: P) {
    const shouldReduceMotion = useReducedMotion();

    if (shouldReduceMotion) {
      return <Component {...props} {...staticProps} />;
    }

    return <Component {...props} />;
  };
}
```

### Animation Context for Global Control

```tsx
// contexts/AnimationContext.tsx
"use client";

import { useReducedMotion } from "framer-motion";
import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";

interface AnimationContextValue {
  isEnabled: boolean;
  setIsEnabled: (enabled: boolean) => void;
  prefersReducedMotion: boolean;
  shouldAnimate: boolean;
}

const AnimationContext = createContext<AnimationContextValue | null>(null);

export function useAnimation() {
  const context = useContext(AnimationContext);
  if (!context) {
    throw new Error("useAnimation must be used within AnimationProvider");
  }
  return context;
}

export function AnimationProvider({ children }: { children: ReactNode }) {
  const [isEnabled, setIsEnabled] = useState(true);
  const prefersReducedMotion = useReducedMotion() ?? false;

  const shouldAnimate = isEnabled && !prefersReducedMotion;

  return (
    <AnimationContext.Provider
      value={{
        isEnabled,
        setIsEnabled,
        prefersReducedMotion,
        shouldAnimate,
      }}
    >
      {children}
    </AnimationContext.Provider>
  );
}

// Animation toggle component
export function AnimationToggle() {
  const { isEnabled, setIsEnabled, prefersReducedMotion } = useAnimation();

  if (prefersReducedMotion) {
    return (
      <p className="text-sm text-gray-500">
        Animations disabled (system preference)
      </p>
    );
  }

  return (
    <label className="flex items-center gap-2 cursor-pointer">
      <input
        type="checkbox"
        checked={isEnabled}
        onChange={(e) => setIsEnabled(e.target.checked)}
        className="sr-only"
      />
      <span
        className={`
          relative inline-flex h-6 w-11 items-center rounded-full transition-colors
          ${isEnabled ? "bg-blue-600" : "bg-gray-300"}
        `}
      >
        <span
          className={`
            inline-block h-4 w-4 transform rounded-full bg-white transition-transform
            ${isEnabled ? "translate-x-6" : "translate-x-1"}
          `}
        />
      </span>
      <span className="text-sm font-medium">
        {isEnabled ? "Animations on" : "Animations off"}
      </span>
    </label>
  );
}
```

### Conditional Animation Wrapper

```tsx
"use client";

import { motion, type MotionProps, type HTMLMotionProps } from "framer-motion";
import { useAnimation } from "@/contexts/AnimationContext";
import { forwardRef, type ElementType, type ComponentPropsWithoutRef } from "react";

type ConditionalMotionProps<T extends ElementType> = {
  as?: T;
  enableMotion?: boolean;
} & HTMLMotionProps<"div"> &
  Omit<ComponentPropsWithoutRef<T>, keyof MotionProps>;

export const ConditionalMotion = forwardRef(function ConditionalMotion<
  T extends ElementType = "div"
>(
  { as, enableMotion = true, children, ...props }: ConditionalMotionProps<T>,
  ref: React.Ref<Element>
) {
  const { shouldAnimate } = useAnimation();
  const Component = as || "div";

  // If animations are disabled, render without motion
  if (!shouldAnimate || !enableMotion) {
    const { initial, animate, exit, variants, transition, whileHover, whileTap, ...rest } = props;
    return (
      <Component ref={ref} {...rest}>
        {children}
      </Component>
    );
  }

  const MotionComponent = motion(Component as ElementType);

  return (
    <MotionComponent ref={ref} {...props}>
      {children}
    </MotionComponent>
  );
});
```

### GPU-Optimized Animations

```tsx
"use client";

import { motion, type Variants } from "framer-motion";

/**
 * GPU-optimized variants that only animate transform and opacity
 * These properties are composited on the GPU and don't trigger layout
 */

export const gpuOptimizedVariants: Variants = {
  hidden: {
    opacity: 0,
    transform: "translateY(20px) scale(0.95)",
  },
  visible: {
    opacity: 1,
    transform: "translateY(0px) scale(1)",
    transition: {
      duration: 0.3,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  },
};

// Using will-change for complex animations
export function OptimizedCard({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      style={{ willChange: "transform, opacity" }}
      onAnimationComplete={() => {
        // Remove will-change after animation to free memory
        // This is handled automatically by Framer Motion in most cases
      }}
      className="p-6 bg-white rounded-xl shadow"
    >
      {children}
    </motion.div>
  );
}

// Avoid animating these properties (cause layout thrashing):
// - width, height
// - top, right, bottom, left
// - margin, padding
// - border-width
// - font-size
// - line-height

// Instead, use these GPU-accelerated properties:
// - transform (translateX, translateY, scale, rotate)
// - opacity
// - filter (blur, brightness, etc.)
```

### Testing Animations

```tsx
// __tests__/animations.test.tsx
import { render, screen } from "@testing-library/react";
import { AnimatedComponent } from "@/components/AnimatedComponent";

// Mock framer-motion for testing
jest.mock("framer-motion", () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  },
  AnimatePresence: ({ children }: any) => children,
  useReducedMotion: () => false,
}));

describe("AnimatedComponent", () => {
  it("renders content correctly", () => {
    render(<AnimatedComponent>Test content</AnimatedComponent>);
    expect(screen.getByText("Test content")).toBeInTheDocument();
  });
});
```

---

## Quick Reference

### Essential Imports

```tsx
import {
  motion,
  AnimatePresence,
  useScroll,
  useTransform,
  useSpring,
  useReducedMotion,
  useMotionValue,
  useInView,
  LayoutGroup,
  Reorder,
  type Variants,
  type Transition,
  type MotionValue,
} from "framer-motion";
```

### Common Patterns Checklist

- [ ] Use variants for reusable animation states
- [ ] Wrap exit animations with AnimatePresence
- [ ] Add layout prop for automatic layout animations
- [ ] Use layoutId for shared element transitions
- [ ] Implement useReducedMotion for accessibility
- [ ] Use GPU-accelerated properties (transform, opacity)
- [ ] Add appropriate transition configurations
- [ ] Test with prefers-reduced-motion enabled
