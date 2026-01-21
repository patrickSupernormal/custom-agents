---
skill: micro-interaction-patterns
version: "1.0.0"
description: "Production-ready patterns for buttons, cursors, hover effects, forms, feedback, and navigation micro-interactions"
used-by:
  - "@interaction-designer"
  - "@ui-engineer"
  - "@animation-engineer"
  - "@react-engineer"
---

# Micro-Interaction Patterns

## Overview

This skill covers delightful, tactile micro-interactions that enhance user experience. Focus is on button states, custom cursors, hover effects, form interactions, feedback patterns, and navigation animations with implementations in CSS/Tailwind, Framer Motion, and GSAP.

---

## 1. Button Interactions

### Scale Effect (CSS/Tailwind)
```css
/* Base button with scale on press */
.btn-scale {
  transition: transform 150ms ease-out, box-shadow 150ms ease-out;
}

.btn-scale:hover {
  transform: scale(1.02);
}

.btn-scale:active {
  transform: scale(0.98);
}

/* Tailwind version */
/* className="transition-transform duration-150 ease-out hover:scale-[1.02] active:scale-[0.98]" */
```

### Ripple Effect (React + CSS)
```tsx
import { useRef, useState } from 'react';

interface Ripple {
  x: number;
  y: number;
  id: number;
}

function RippleButton({ children, onClick, className }: {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
}) {
  const [ripples, setRipples] = useState<Ripple[]>([]);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const createRipple = (e: React.MouseEvent<HTMLButtonElement>) => {
    const button = buttonRef.current;
    if (!button) return;

    const rect = button.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const id = Date.now();

    setRipples((prev) => [...prev, { x, y, id }]);
    setTimeout(() => {
      setRipples((prev) => prev.filter((r) => r.id !== id));
    }, 600);

    onClick?.();
  };

  return (
    <button
      ref={buttonRef}
      onClick={createRipple}
      className={`relative overflow-hidden ${className}`}
    >
      {children}
      {ripples.map((ripple) => (
        <span
          key={ripple.id}
          className="absolute rounded-full bg-white/30 animate-ripple pointer-events-none"
          style={{
            left: ripple.x,
            top: ripple.y,
            transform: 'translate(-50%, -50%)',
          }}
        />
      ))}
    </button>
  );
}

/* Add to globals.css */
/*
@keyframes ripple {
  0% {
    width: 0;
    height: 0;
    opacity: 0.5;
  }
  100% {
    width: 500px;
    height: 500px;
    opacity: 0;
  }
}

.animate-ripple {
  animation: ripple 600ms ease-out forwards;
}
*/
```

### Magnetic Button (Framer Motion)
```tsx
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { useRef } from 'react';

function MagneticButton({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLButtonElement>(null);

  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const springConfig = { damping: 15, stiffness: 150 };
  const xSpring = useSpring(x, springConfig);
  const ySpring = useSpring(y, springConfig);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    // Magnetic pull strength (0.3 = 30% of distance)
    const pullStrength = 0.3;
    x.set((e.clientX - centerX) * pullStrength);
    y.set((e.clientY - centerY) * pullStrength);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
  };

  return (
    <motion.button
      ref={ref}
      style={{ x: xSpring, y: ySpring }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className="px-6 py-3 bg-blue-600 text-white rounded-lg"
    >
      {children}
    </motion.button>
  );
}
```

### Loading Button States (Framer Motion)
```tsx
import { motion, AnimatePresence } from 'framer-motion';

type ButtonState = 'idle' | 'loading' | 'success' | 'error';

function LoadingButton({
  state,
  onClick,
  children,
}: {
  state: ButtonState;
  onClick: () => void;
  children: React.ReactNode;
}) {
  const variants = {
    idle: { width: 'auto' },
    loading: { width: 48 },
    success: { width: 48, backgroundColor: '#22c55e' },
    error: { width: 48, backgroundColor: '#ef4444' },
  };

  return (
    <motion.button
      onClick={onClick}
      disabled={state !== 'idle'}
      animate={state}
      variants={variants}
      transition={{ duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
      className="relative h-12 px-6 bg-blue-600 text-white rounded-lg overflow-hidden disabled:cursor-not-allowed"
    >
      <AnimatePresence mode="wait">
        {state === 'idle' && (
          <motion.span
            key="idle"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {children}
          </motion.span>
        )}
        {state === 'loading' && (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1, rotate: 360 }}
            exit={{ opacity: 0 }}
            transition={{ rotate: { repeat: Infinity, duration: 1, ease: 'linear' } }}
            className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
          />
        )}
        {state === 'success' && (
          <motion.svg
            key="success"
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-5 h-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clipRule="evenodd"
            />
          </motion.svg>
        )}
        {state === 'error' && (
          <motion.svg
            key="error"
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-5 h-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clipRule="evenodd"
            />
          </motion.svg>
        )}
      </AnimatePresence>
    </motion.button>
  );
}
```

---

## 2. Custom Cursor Effects

### Basic Cursor Follower (GSAP)
```tsx
import { useEffect, useRef } from 'react';
import gsap from 'gsap';

function CustomCursor() {
  const cursorRef = useRef<HTMLDivElement>(null);
  const cursorDotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const cursor = cursorRef.current;
    const cursorDot = cursorDotRef.current;
    if (!cursor || !cursorDot) return;

    const moveCursor = (e: MouseEvent) => {
      // Outer cursor with lag
      gsap.to(cursor, {
        x: e.clientX,
        y: e.clientY,
        duration: 0.5,
        ease: 'power3.out',
      });

      // Inner dot follows immediately
      gsap.to(cursorDot, {
        x: e.clientX,
        y: e.clientY,
        duration: 0.1,
      });
    };

    window.addEventListener('mousemove', moveCursor);
    return () => window.removeEventListener('mousemove', moveCursor);
  }, []);

  return (
    <>
      <div
        ref={cursorRef}
        className="fixed top-0 left-0 w-10 h-10 -translate-x-1/2 -translate-y-1/2 border-2 border-blue-500 rounded-full pointer-events-none z-[9999] mix-blend-difference"
      />
      <div
        ref={cursorDotRef}
        className="fixed top-0 left-0 w-2 h-2 -translate-x-1/2 -translate-y-1/2 bg-blue-500 rounded-full pointer-events-none z-[9999]"
      />
    </>
  );
}
```

### Context-Aware Cursor (Framer Motion)
```tsx
import { motion, useMotionValue, useSpring } from 'framer-motion';
import { createContext, useContext, useState, useEffect } from 'react';

type CursorVariant = 'default' | 'hover' | 'click' | 'text' | 'hidden';

interface CursorContextType {
  setCursorVariant: (variant: CursorVariant) => void;
}

const CursorContext = createContext<CursorContextType>({ setCursorVariant: () => {} });

export function CursorProvider({ children }: { children: React.ReactNode }) {
  const [variant, setVariant] = useState<CursorVariant>('default');
  const cursorX = useMotionValue(0);
  const cursorY = useMotionValue(0);

  const springConfig = { damping: 25, stiffness: 300 };
  const cursorXSpring = useSpring(cursorX, springConfig);
  const cursorYSpring = useSpring(cursorY, springConfig);

  useEffect(() => {
    const moveCursor = (e: MouseEvent) => {
      cursorX.set(e.clientX);
      cursorY.set(e.clientY);
    };
    window.addEventListener('mousemove', moveCursor);
    return () => window.removeEventListener('mousemove', moveCursor);
  }, [cursorX, cursorY]);

  const variants = {
    default: { width: 32, height: 32, backgroundColor: 'transparent', border: '2px solid #3b82f6' },
    hover: { width: 64, height: 64, backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '2px solid #3b82f6' },
    click: { width: 48, height: 48, backgroundColor: 'rgba(59, 130, 246, 0.3)', border: '2px solid #3b82f6' },
    text: { width: 4, height: 24, borderRadius: 0, backgroundColor: '#3b82f6', border: 'none' },
    hidden: { width: 0, height: 0, opacity: 0 },
  };

  return (
    <CursorContext.Provider value={{ setCursorVariant: setVariant }}>
      <motion.div
        className="fixed top-0 left-0 rounded-full pointer-events-none z-[9999] -translate-x-1/2 -translate-y-1/2"
        style={{ x: cursorXSpring, y: cursorYSpring }}
        variants={variants}
        animate={variant}
        transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      />
      {children}
    </CursorContext.Provider>
  );
}

export function useCursor() {
  return useContext(CursorContext);
}

// Usage in components
function InteractiveLink({ href, children }: { href: string; children: React.ReactNode }) {
  const { setCursorVariant } = useCursor();

  return (
    <a
      href={href}
      onMouseEnter={() => setCursorVariant('hover')}
      onMouseLeave={() => setCursorVariant('default')}
    >
      {children}
    </a>
  );
}
```

### Magnetic Cursor Effect (GSAP)
```tsx
import { useEffect, useRef } from 'react';
import gsap from 'gsap';

function MagneticElement({ children }: { children: React.ReactNode }) {
  const elementRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = element.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      const distanceX = e.clientX - centerX;
      const distanceY = e.clientY - centerY;

      // Check if mouse is within magnetic range
      const magneticRange = 100;
      const distance = Math.sqrt(distanceX ** 2 + distanceY ** 2);

      if (distance < magneticRange) {
        const strength = 1 - distance / magneticRange;
        gsap.to(element, {
          x: distanceX * strength * 0.4,
          y: distanceY * strength * 0.4,
          duration: 0.3,
          ease: 'power2.out',
        });
      }
    };

    const handleMouseLeave = () => {
      gsap.to(element, {
        x: 0,
        y: 0,
        duration: 0.5,
        ease: 'elastic.out(1, 0.3)',
      });
    };

    element.addEventListener('mousemove', handleMouseMove);
    element.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      element.removeEventListener('mousemove', handleMouseMove);
      element.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  return <div ref={elementRef}>{children}</div>;
}
```

---

## 3. Hover Effects

### Card Lift Effect (CSS/Tailwind)
```css
.card-lift {
  transition: transform 300ms ease-out, box-shadow 300ms ease-out;
}

.card-lift:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.15);
}

/* Tailwind */
/* className="transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-[0_20px_40px_-12px_rgba(0,0,0,0.15)]" */
```

### Border Glow Effect (CSS)
```css
.border-glow {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
}

.border-glow::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 2px;
  border-radius: inherit;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-mask:
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 300ms ease-out;
}

.border-glow:hover::before {
  opacity: 1;
}
```

### Image Zoom with Overlay (Framer Motion)
```tsx
import { motion } from 'framer-motion';

function ImageCard({ src, alt, title }: { src: string; alt: string; title: string }) {
  return (
    <motion.div
      className="relative overflow-hidden rounded-xl cursor-pointer"
      whileHover="hover"
    >
      <motion.img
        src={src}
        alt={alt}
        className="w-full h-64 object-cover"
        variants={{
          hover: { scale: 1.1 },
        }}
        transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
      />
      <motion.div
        className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent flex items-end p-6"
        variants={{
          hover: { opacity: 1 },
        }}
        initial={{ opacity: 0 }}
        transition={{ duration: 0.3 }}
      >
        <motion.h3
          className="text-white text-xl font-semibold"
          variants={{
            hover: { y: 0, opacity: 1 },
          }}
          initial={{ y: 20, opacity: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          {title}
        </motion.h3>
      </motion.div>
    </motion.div>
  );
}
```

### Animated Underline Links (CSS)
```css
/* Slide from left */
.underline-slide {
  position: relative;
}

.underline-slide::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 300ms ease-out;
}

.underline-slide:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}

/* Expand from center */
.underline-center {
  position: relative;
}

.underline-center::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: currentColor;
  transform: translateX(-50%) scaleX(0);
  transition: transform 300ms ease-out;
}

.underline-center:hover::after {
  transform: translateX(-50%) scaleX(1);
}

/* Gradient underline */
.underline-gradient {
  position: relative;
}

.underline-gradient::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 300ms ease-out;
}

.underline-gradient:hover::after {
  transform: scaleX(1);
}
```

### 3D Tilt Card (Framer Motion)
```tsx
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { useRef } from 'react';

function TiltCard({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);

  const x = useMotionValue(0.5);
  const y = useMotionValue(0.5);

  const rotateX = useTransform(y, [0, 1], [10, -10]);
  const rotateY = useTransform(x, [0, 1], [-10, 10]);

  const springConfig = { damping: 20, stiffness: 300 };
  const rotateXSpring = useSpring(rotateX, springConfig);
  const rotateYSpring = useSpring(rotateY, springConfig);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    x.set((e.clientX - rect.left) / rect.width);
    y.set((e.clientY - rect.top) / rect.height);
  };

  const handleMouseLeave = () => {
    x.set(0.5);
    y.set(0.5);
  };

  return (
    <motion.div
      ref={ref}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        rotateX: rotateXSpring,
        rotateY: rotateYSpring,
        transformStyle: 'preserve-3d',
        perspective: 1000,
      }}
      className="bg-white rounded-xl p-6 shadow-lg"
    >
      {children}
    </motion.div>
  );
}
```

---

## 4. Form Interactions

### Floating Label Input (CSS/React)
```tsx
import { useState } from 'react';

function FloatingInput({
  label,
  type = 'text',
  id,
}: {
  label: string;
  type?: string;
  id: string;
}) {
  const [isFocused, setIsFocused] = useState(false);
  const [hasValue, setHasValue] = useState(false);

  const isFloating = isFocused || hasValue;

  return (
    <div className="relative">
      <input
        type={type}
        id={id}
        className="w-full px-4 pt-5 pb-2 border-2 border-gray-300 rounded-lg outline-none transition-colors duration-200 focus:border-blue-500 peer"
        onFocus={() => setIsFocused(true)}
        onBlur={(e) => {
          setIsFocused(false);
          setHasValue(e.target.value !== '');
        }}
        onChange={(e) => setHasValue(e.target.value !== '')}
      />
      <label
        htmlFor={id}
        className={`absolute left-4 transition-all duration-200 pointer-events-none ${
          isFloating
            ? 'top-1 text-xs text-blue-500'
            : 'top-1/2 -translate-y-1/2 text-gray-500'
        }`}
      >
        {label}
      </label>
    </div>
  );
}
```

### Focus Ring Animation (CSS)
```css
.input-focus-ring {
  position: relative;
}

.input-focus-ring::after {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 12px;
  border: 2px solid transparent;
  transition: border-color 200ms ease-out, box-shadow 200ms ease-out;
  pointer-events: none;
}

.input-focus-ring:focus-within::after {
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}
```

### Validation Shake Effect (Framer Motion)
```tsx
import { motion, useAnimation } from 'framer-motion';
import { useEffect } from 'react';

function ShakeInput({
  error,
  children,
}: {
  error: boolean;
  children: React.ReactNode;
}) {
  const controls = useAnimation();

  useEffect(() => {
    if (error) {
      controls.start({
        x: [0, -10, 10, -10, 10, -5, 5, 0],
        transition: { duration: 0.5 },
      });
    }
  }, [error, controls]);

  return (
    <motion.div animate={controls}>
      {children}
      {error && (
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-red-500 text-sm mt-1"
        >
          This field is required
        </motion.p>
      )}
    </motion.div>
  );
}
```

### Input Character Counter (Framer Motion)
```tsx
import { motion } from 'framer-motion';
import { useState } from 'react';

function CharacterCountInput({
  maxLength,
  label,
}: {
  maxLength: number;
  label: string;
}) {
  const [value, setValue] = useState('');
  const remaining = maxLength - value.length;
  const isNearLimit = remaining <= 20;
  const isAtLimit = remaining <= 0;

  return (
    <div className="relative">
      <label className="block text-sm font-medium mb-1">{label}</label>
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value.slice(0, maxLength))}
        className="w-full p-3 border rounded-lg resize-none"
        rows={4}
      />
      <motion.span
        className={`absolute bottom-2 right-2 text-sm ${
          isAtLimit ? 'text-red-500' : isNearLimit ? 'text-amber-500' : 'text-gray-400'
        }`}
        animate={{
          scale: isNearLimit ? [1, 1.1, 1] : 1,
        }}
        transition={{ duration: 0.2 }}
      >
        {remaining}
      </motion.span>
    </div>
  );
}
```

---

## 5. Feedback Patterns

### Success Checkmark Animation (Framer Motion)
```tsx
import { motion } from 'framer-motion';

function SuccessCheckmark({ show }: { show: boolean }) {
  if (!show) return null;

  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      className="w-16 h-16 rounded-full bg-green-500 flex items-center justify-center"
    >
      <motion.svg
        viewBox="0 0 24 24"
        className="w-8 h-8 text-white"
        initial="hidden"
        animate="visible"
      >
        <motion.path
          d="M5 13l4 4L19 7"
          fill="none"
          stroke="currentColor"
          strokeWidth={3}
          strokeLinecap="round"
          strokeLinejoin="round"
          variants={{
            hidden: { pathLength: 0 },
            visible: { pathLength: 1 },
          }}
          transition={{ duration: 0.4, delay: 0.2, ease: 'easeOut' }}
        />
      </motion.svg>
    </motion.div>
  );
}
```

### Toast Notification (Framer Motion)
```tsx
import { motion, AnimatePresence } from 'framer-motion';

interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info';
}

function ToastContainer({ toasts }: { toasts: Toast[] }) {
  const typeStyles = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    info: 'bg-blue-500',
  };

  return (
    <div className="fixed bottom-4 right-4 flex flex-col gap-2 z-50">
      <AnimatePresence mode="popLayout">
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            layout
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, x: 100, scale: 0.9 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className={`${typeStyles[toast.type]} text-white px-4 py-3 rounded-lg shadow-lg min-w-[280px]`}
          >
            {toast.message}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
```

### Skeleton Loading (CSS)
```css
.skeleton {
  background: linear-gradient(
    90deg,
    #e5e7eb 0%,
    #f3f4f6 50%,
    #e5e7eb 100%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
  border-radius: 4px;
}

@keyframes skeleton-shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Usage */
/*
<div class="skeleton h-4 w-3/4 mb-2"></div>
<div class="skeleton h-4 w-1/2"></div>
*/
```

### Skeleton Loading Component (React)
```tsx
function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={`animate-pulse bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 bg-[length:200%_100%] rounded ${className}`}
      style={{
        animation: 'shimmer 1.5s ease-in-out infinite',
      }}
    />
  );
}

function CardSkeleton() {
  return (
    <div className="p-4 border rounded-lg">
      <Skeleton className="h-48 w-full mb-4" />
      <Skeleton className="h-4 w-3/4 mb-2" />
      <Skeleton className="h-4 w-1/2 mb-4" />
      <Skeleton className="h-8 w-24" />
    </div>
  );
}
```

### Progress Indicator (Framer Motion)
```tsx
import { motion } from 'framer-motion';

function ProgressBar({ progress }: { progress: number }) {
  return (
    <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
      <motion.div
        className="h-full bg-blue-500"
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
      />
    </div>
  );
}

function CircularProgress({ progress }: { progress: number }) {
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <svg width="100" height="100" className="-rotate-90">
      <circle
        cx="50"
        cy="50"
        r="45"
        stroke="#e5e7eb"
        strokeWidth="8"
        fill="none"
      />
      <motion.circle
        cx="50"
        cy="50"
        r="45"
        stroke="#3b82f6"
        strokeWidth="8"
        fill="none"
        strokeLinecap="round"
        initial={{ strokeDashoffset: circumference }}
        animate={{ strokeDashoffset }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        style={{
          strokeDasharray: circumference,
        }}
      />
    </svg>
  );
}
```

---

## 6. Navigation Interactions

### Hamburger to X Morph (Framer Motion)
```tsx
import { motion } from 'framer-motion';

function HamburgerMenu({ isOpen, toggle }: { isOpen: boolean; toggle: () => void }) {
  const lineVariants = {
    closed: { rotate: 0, y: 0 },
    open: (custom: number) => ({
      rotate: custom === 1 ? 45 : custom === 3 ? -45 : 0,
      y: custom === 1 ? 8 : custom === 3 ? -8 : 0,
      opacity: custom === 2 ? 0 : 1,
    }),
  };

  return (
    <button
      onClick={toggle}
      className="w-10 h-10 flex flex-col justify-center items-center gap-1.5"
      aria-label={isOpen ? 'Close menu' : 'Open menu'}
      aria-expanded={isOpen}
    >
      {[1, 2, 3].map((line) => (
        <motion.span
          key={line}
          custom={line}
          variants={lineVariants}
          animate={isOpen ? 'open' : 'closed'}
          transition={{ duration: 0.3 }}
          className="w-6 h-0.5 bg-current block"
        />
      ))}
    </button>
  );
}
```

### Dropdown Menu (Framer Motion)
```tsx
import { motion, AnimatePresence } from 'framer-motion';
import { useState, useRef, useEffect } from 'react';

function Dropdown({
  trigger,
  children,
}: {
  trigger: React.ReactNode;
  children: React.ReactNode;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div ref={dropdownRef} className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        {trigger}
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.15, ease: [0.25, 0.1, 0.25, 1] }}
            className="absolute top-full left-0 mt-2 bg-white rounded-lg shadow-lg border py-2 min-w-[200px] z-50"
            role="menu"
          >
            {children}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function DropdownItem({
  children,
  onClick,
}: {
  children: React.ReactNode;
  onClick?: () => void;
}) {
  return (
    <motion.button
      onClick={onClick}
      className="w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors"
      whileHover={{ x: 4 }}
      role="menuitem"
    >
      {children}
    </motion.button>
  );
}
```

### Mobile Drawer (Framer Motion)
```tsx
import { motion, AnimatePresence } from 'framer-motion';

function MobileDrawer({
  isOpen,
  onClose,
  children,
}: {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 z-40"
          />

          {/* Drawer */}
          <motion.div
            initial={{ x: '-100%' }}
            animate={{ x: 0 }}
            exit={{ x: '-100%' }}
            transition={{ type: 'spring', damping: 30, stiffness: 300 }}
            className="fixed top-0 left-0 bottom-0 w-80 bg-white z-50 shadow-xl"
            role="dialog"
            aria-modal="true"
          >
            <button
              onClick={onClose}
              className="absolute top-4 right-4 p-2"
              aria-label="Close menu"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

### Tab Indicator (Framer Motion)
```tsx
import { motion } from 'framer-motion';
import { useState, useRef, useEffect } from 'react';

function Tabs({
  tabs,
  activeTab,
  onChange,
}: {
  tabs: string[];
  activeTab: number;
  onChange: (index: number) => void;
}) {
  const [indicatorStyle, setIndicatorStyle] = useState({ left: 0, width: 0 });
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);

  useEffect(() => {
    const activeTabElement = tabRefs.current[activeTab];
    if (activeTabElement) {
      setIndicatorStyle({
        left: activeTabElement.offsetLeft,
        width: activeTabElement.offsetWidth,
      });
    }
  }, [activeTab]);

  return (
    <div className="relative" role="tablist">
      <div className="flex gap-2">
        {tabs.map((tab, index) => (
          <button
            key={tab}
            ref={(el) => { tabRefs.current[index] = el; }}
            onClick={() => onChange(index)}
            className={`px-4 py-2 relative z-10 transition-colors ${
              activeTab === index ? 'text-blue-600' : 'text-gray-600'
            }`}
            role="tab"
            aria-selected={activeTab === index}
          >
            {tab}
          </button>
        ))}
      </div>
      <motion.div
        className="absolute bottom-0 h-0.5 bg-blue-600"
        animate={indicatorStyle}
        transition={{ type: 'spring', damping: 30, stiffness: 300 }}
      />
    </div>
  );
}
```

---

## 7. Timing Guidelines and Easing Reference

### Duration Guidelines

| Interaction Type | Duration | Use Case |
|------------------|----------|----------|
| Instant feedback | 50-100ms | Button active states, checkboxes |
| Quick response | 100-200ms | Hover effects, tooltips, small reveals |
| Standard | 200-300ms | Modals, dropdowns, page elements |
| Deliberate | 300-500ms | Complex transitions, accordions |
| Dramatic | 500-1000ms | Page transitions, onboarding |

### Easing Functions

```css
/* CSS Custom Properties */
:root {
  /* Standard easings */
  --ease-out: cubic-bezier(0.25, 0.1, 0.25, 1);
  --ease-in: cubic-bezier(0.42, 0, 1, 1);
  --ease-in-out: cubic-bezier(0.42, 0, 0.58, 1);

  /* Expressive easings */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-out-elastic: cubic-bezier(0.68, -0.6, 0.32, 1.6);
  --ease-in-out-circ: cubic-bezier(0.85, 0, 0.15, 1);

  /* Smooth deceleration (recommended for most UI) */
  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
}
```

```typescript
// Framer Motion / GSAP easing presets
const easings = {
  // Standard (matches CSS ease-out)
  standard: [0.25, 0.1, 0.25, 1],

  // Emphasized for entrances
  emphasized: [0.2, 0, 0, 1],

  // Decelerated for exits
  decelerated: [0, 0, 0.2, 1],

  // Smooth for most UI (Material Design)
  smooth: [0.4, 0, 0.2, 1],

  // Bounce for playful feedback
  bounce: [0.68, -0.6, 0.32, 1.6],

  // Sharp for quick interactions
  sharp: [0.4, 0, 0.6, 1],
};

// GSAP named easings
const gsapEasings = {
  standard: 'power2.out',
  entrance: 'power3.out',
  exit: 'power2.in',
  bounce: 'back.out(1.7)',
  elastic: 'elastic.out(1, 0.3)',
  smooth: 'power4.out',
};
```

### Recommended Combinations

| Pattern | Duration | Easing |
|---------|----------|--------|
| Button press | 100ms | ease-out |
| Button release | 200ms | ease-out-back |
| Hover enter | 200ms | ease-out |
| Hover leave | 300ms | ease-out |
| Modal open | 300ms | ease-out-expo |
| Modal close | 200ms | ease-in |
| Dropdown open | 200ms | ease-out |
| Dropdown close | 150ms | ease-in |
| Toast enter | 300ms | ease-out-back |
| Toast exit | 200ms | ease-in |
| Page transition | 400ms | ease-in-out |

---

## 8. Accessibility Considerations

### Respecting Reduced Motion
```tsx
import { useReducedMotion } from 'framer-motion';

function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      animate={{ x: 100 }}
      transition={shouldReduceMotion ? { duration: 0 } : { duration: 0.3 }}
    >
      Content
    </motion.div>
  );
}

// CSS approach
/*
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
*/
```

### Custom Hook for Reduced Motion
```tsx
import { useEffect, useState } from 'react';

function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(event.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return prefersReducedMotion;
}
```

### Focus Management
```tsx
// Ensure focus is visible during keyboard navigation
function FocusVisibleButton({ children }: { children: React.ReactNode }) {
  return (
    <button className="focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
      {children}
    </button>
  );
}

// Skip animation on focus for screen reader users
function AccessibleHoverCard({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      whileHover={{ y: -8 }}
      // Don't animate on focus - screen reader users don't benefit
      whileFocus={{ y: 0 }}
      className="focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
      tabIndex={0}
    >
      {children}
    </motion.div>
  );
}
```

### Touch Considerations
```tsx
// Larger touch targets for mobile
function TouchFriendlyButton({ children, onClick }: { children: React.ReactNode; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="min-h-[44px] min-w-[44px] p-3" // WCAG minimum 44x44px
    >
      {children}
    </button>
  );
}

// Disable hover effects on touch devices
const isTouchDevice = typeof window !== 'undefined' && 'ontouchstart' in window;

function ResponsiveHoverCard({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      whileHover={isTouchDevice ? {} : { scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      {children}
    </motion.div>
  );
}
```

### ARIA for Loading States
```tsx
function LoadingButton({
  isLoading,
  children,
  onClick,
}: {
  isLoading: boolean;
  children: React.ReactNode;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      disabled={isLoading}
      aria-busy={isLoading}
      aria-disabled={isLoading}
    >
      {isLoading ? (
        <>
          <span className="sr-only">Loading</span>
          <span aria-hidden="true">
            <Spinner />
          </span>
        </>
      ) : (
        children
      )}
    </button>
  );
}
```

---

## Common Pitfalls

1. **Excessive Animation** - Not every element needs to animate; reserve motion for meaningful feedback
2. **Ignoring Reduced Motion** - Always implement `prefers-reduced-motion` fallbacks
3. **Animating Layout Properties** - Stick to `transform` and `opacity` for performance
4. **Too Slow Interactions** - Keep micro-interactions under 300ms to feel responsive
5. **Missing Focus States** - Ensure keyboard users see clear focus indicators
6. **Touch Target Size** - Maintain minimum 44x44px for touch interactions
7. **Conflicting Animations** - Avoid multiple competing animations on the same element
8. **No Exit Animations** - Elements should animate out, not just disappear
9. **Cursor Hiding Native** - Always keep fallback for the native cursor on touch/accessibility
10. **Motion Sickness** - Avoid large-scale parallax and continuous motion
