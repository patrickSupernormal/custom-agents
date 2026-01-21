---
name: webgl-r3f-patterns
version: 1.0.0
used-by:
  - webgl-developer
  - react-engineer
  - animation-engineer
---

# WebGL and React Three Fiber Patterns

Production-ready patterns for building 3D web experiences with React Three Fiber, Three.js, and Drei.

## 1. Project Setup

### Dependencies

```bash
# Core dependencies
npm install three @react-three/fiber @react-three/drei

# Optional but recommended
npm install @react-three/postprocessing  # Post-processing effects
npm install @react-three/rapier          # Physics
npm install leva                          # Debug GUI
npm install maath                         # Math utilities
npm install zustand                       # State management

# TypeScript types
npm install -D @types/three
```

### Next.js Integration

```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['three'],
  webpack: (config) => {
    config.externals.push({
      'sharp': 'commonjs sharp',
    })
    return config
  },
}

module.exports = nextConfig
```

### Dynamic Import Pattern (SSR-Safe)

```typescript
// components/Scene.tsx
'use client'

import dynamic from 'next/dynamic'
import { Suspense } from 'react'

const Canvas = dynamic(
  () => import('@react-three/fiber').then((mod) => mod.Canvas),
  { ssr: false }
)

export function Scene({ children }: { children: React.ReactNode }) {
  return (
    <div className="h-screen w-full">
      <Suspense fallback={<div className="h-full w-full bg-black" />}>
        <Canvas>{children}</Canvas>
      </Suspense>
    </div>
  )
}
```

### App Structure

```typescript
// app/page.tsx
import { Scene } from '@/components/Scene'
import { Experience } from '@/components/Experience'

export default function Home() {
  return (
    <main className="relative h-screen w-full">
      <Scene>
        <Experience />
      </Scene>
      {/* DOM overlay content */}
      <div className="pointer-events-none absolute inset-0">
        <h1 className="p-8 text-4xl text-white">3D Experience</h1>
      </div>
    </main>
  )
}
```

---

## 2. Canvas Configuration

### Basic Canvas Setup

```typescript
import { Canvas } from '@react-three/fiber'
import * as THREE from 'three'

export function Scene({ children }: { children: React.ReactNode }) {
  return (
    <Canvas
      // Camera configuration
      camera={{
        position: [0, 2, 5],
        fov: 45,
        near: 0.1,
        far: 1000,
      }}
      // Renderer configuration
      gl={{
        antialias: true,
        alpha: false,
        powerPreference: 'high-performance',
        outputColorSpace: THREE.SRGBColorSpace,
        toneMapping: THREE.ACESFilmicToneMapping,
        toneMappingExposure: 1.2,
      }}
      // Shadows
      shadows="soft" // or true, 'basic', 'percentage', 'soft', 'variance'
      // Performance
      dpr={[1, 2]} // Device pixel ratio clamp
      // Event handling
      eventSource={document.body}
      eventPrefix="client"
    >
      {children}
    </Canvas>
  )
}
```

### Advanced Canvas with All Options

```typescript
import { Canvas, RootState } from '@react-three/fiber'
import { Perf } from 'r3f-perf'
import * as THREE from 'three'

interface SceneProps {
  children: React.ReactNode
  debug?: boolean
}

export function Scene({ children, debug = false }: SceneProps) {
  const handleCreated = (state: RootState) => {
    // Access Three.js objects after canvas creation
    state.gl.setClearColor('#000000', 1)
    state.scene.fog = new THREE.Fog('#000000', 10, 50)
  }

  return (
    <Canvas
      camera={{
        position: [0, 5, 10],
        fov: 50,
        near: 0.1,
        far: 200,
      }}
      gl={{
        antialias: true,
        alpha: false,
        stencil: false,
        depth: true,
        powerPreference: 'high-performance',
        outputColorSpace: THREE.SRGBColorSpace,
        toneMapping: THREE.ACESFilmicToneMapping,
        toneMappingExposure: 1.0,
      }}
      shadows={{
        enabled: true,
        type: THREE.PCFSoftShadowMap,
      }}
      dpr={[1, 2]}
      frameloop="demand" // 'always', 'demand', 'never'
      onCreated={handleCreated}
      flat // Disable automatic sRGB color management
      linear // Disable automatic gamma correction
    >
      {debug && <Perf position="top-left" />}
      {children}
    </Canvas>
  )
}
```

### Responsive Canvas

```typescript
import { Canvas } from '@react-three/fiber'
import { AdaptiveDpr, AdaptiveEvents, Preload } from '@react-three/drei'

export function ResponsiveScene({ children }: { children: React.ReactNode }) {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 45 }}
      dpr={[1, 2]}
    >
      {/* Automatically adjusts DPR based on performance */}
      <AdaptiveDpr pixelated />
      {/* Automatically adjusts event handling */}
      <AdaptiveEvents />
      {/* Preload all assets */}
      <Preload all />
      {children}
    </Canvas>
  )
}
```

---

## 3. Component Patterns

### Basic Mesh Component

```typescript
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface BoxProps {
  position?: [number, number, number]
  color?: string
  speed?: number
}

export function Box({ position = [0, 0, 0], color = '#ff6b6b', speed = 1 }: BoxProps) {
  const meshRef = useRef<THREE.Mesh>(null)

  useFrame((state, delta) => {
    if (!meshRef.current) return
    meshRef.current.rotation.x += delta * speed
    meshRef.current.rotation.y += delta * speed * 0.5
  })

  return (
    <mesh ref={meshRef} position={position} castShadow receiveShadow>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={color} />
    </mesh>
  )
}
```

### GLTF Model Loading

```typescript
import { useRef, useEffect } from 'react'
import { useGLTF, useAnimations } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface ModelProps {
  url: string
  position?: [number, number, number]
  scale?: number
  animation?: string
}

export function Model({ url, position = [0, 0, 0], scale = 1, animation }: ModelProps) {
  const groupRef = useRef<THREE.Group>(null)
  const { scene, animations } = useGLTF(url)
  const { actions, names } = useAnimations(animations, groupRef)

  useEffect(() => {
    // Clone scene for multiple instances
    scene.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        child.castShadow = true
        child.receiveShadow = true
      }
    })
  }, [scene])

  useEffect(() => {
    if (animation && actions[animation]) {
      actions[animation]?.reset().fadeIn(0.5).play()
      return () => {
        actions[animation]?.fadeOut(0.5)
      }
    }
  }, [animation, actions])

  return (
    <group ref={groupRef} position={position} scale={scale}>
      <primitive object={scene} />
    </group>
  )
}

// Preload model
useGLTF.preload('/models/character.glb')
```

### Instanced Mesh Pattern

```typescript
import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface InstancedBoxesProps {
  count?: number
  range?: number
}

export function InstancedBoxes({ count = 1000, range = 10 }: InstancedBoxesProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  const dummy = useMemo(() => new THREE.Object3D(), [])

  // Generate random positions
  const particles = useMemo(() => {
    const temp = []
    for (let i = 0; i < count; i++) {
      const position = new THREE.Vector3(
        (Math.random() - 0.5) * range,
        (Math.random() - 0.5) * range,
        (Math.random() - 0.5) * range
      )
      const scale = 0.2 + Math.random() * 0.3
      const speed = 0.1 + Math.random() * 0.5
      temp.push({ position, scale, speed })
    }
    return temp
  }, [count, range])

  useFrame((state) => {
    if (!meshRef.current) return

    particles.forEach((particle, i) => {
      const t = state.clock.elapsedTime * particle.speed
      dummy.position.copy(particle.position)
      dummy.position.y += Math.sin(t + i) * 0.1
      dummy.rotation.set(t * 0.5, t * 0.3, t * 0.2)
      dummy.scale.setScalar(particle.scale)
      dummy.updateMatrix()
      meshRef.current!.setMatrixAt(i, dummy.matrix)
    })

    meshRef.current.instanceMatrix.needsUpdate = true
  })

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]} castShadow>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#88ccff" />
    </instancedMesh>
  )
}
```

### Instanced Mesh with Individual Colors

```typescript
import { useRef, useMemo } from 'react'
import * as THREE from 'three'

interface ColoredInstancesProps {
  count?: number
}

export function ColoredInstances({ count = 100 }: ColoredInstancesProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null)

  const { matrices, colors } = useMemo(() => {
    const matrices: THREE.Matrix4[] = []
    const colors: Float32Array = new Float32Array(count * 3)
    const dummy = new THREE.Object3D()
    const color = new THREE.Color()

    for (let i = 0; i < count; i++) {
      dummy.position.set(
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10
      )
      dummy.rotation.set(
        Math.random() * Math.PI,
        Math.random() * Math.PI,
        Math.random() * Math.PI
      )
      dummy.scale.setScalar(0.5 + Math.random() * 0.5)
      dummy.updateMatrix()
      matrices.push(dummy.matrix.clone())

      // HSL color for nice distribution
      color.setHSL(Math.random(), 0.7, 0.5)
      colors[i * 3] = color.r
      colors[i * 3 + 1] = color.g
      colors[i * 3 + 2] = color.b
    }

    return { matrices, colors }
  }, [count])

  // Set matrices and colors on mount
  useMemo(() => {
    if (!meshRef.current) return
    matrices.forEach((matrix, i) => {
      meshRef.current!.setMatrixAt(i, matrix)
    })
    meshRef.current.geometry.setAttribute(
      'color',
      new THREE.InstancedBufferAttribute(colors, 3)
    )
  }, [matrices, colors])

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[0.5, 32, 32]} />
      <meshStandardMaterial vertexColors />
    </instancedMesh>
  )
}
```

---

## 4. Materials

### Standard Material Variants

```typescript
import * as THREE from 'three'
import { useTexture } from '@react-three/drei'

// Basic standard material
export function BasicMaterial() {
  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        color="#88aaff"
        roughness={0.3}
        metalness={0.8}
        envMapIntensity={1}
      />
    </mesh>
  )
}

// Physical material (extends standard with more properties)
export function PhysicalMaterial() {
  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshPhysicalMaterial
        color="#ffffff"
        roughness={0.1}
        metalness={0}
        clearcoat={1}
        clearcoatRoughness={0.1}
        transmission={0.9}
        thickness={2}
        ior={1.5}
        envMapIntensity={1}
      />
    </mesh>
  )
}

// Textured material
export function TexturedMaterial() {
  const textures = useTexture({
    map: '/textures/albedo.jpg',
    normalMap: '/textures/normal.jpg',
    roughnessMap: '/textures/roughness.jpg',
    aoMap: '/textures/ao.jpg',
    displacementMap: '/textures/height.jpg',
  })

  // Configure texture properties
  Object.values(textures).forEach((texture) => {
    if (texture) {
      texture.wrapS = texture.wrapT = THREE.RepeatWrapping
      texture.repeat.set(2, 2)
    }
  })

  return (
    <mesh>
      <planeGeometry args={[10, 10, 128, 128]} />
      <meshStandardMaterial
        {...textures}
        displacementScale={0.2}
        aoMapIntensity={0.5}
      />
    </mesh>
  )
}
```

### Custom Shader Material

```typescript
import { useRef, useMemo } from 'react'
import { useFrame, extend, Object3DNode } from '@react-three/fiber'
import { shaderMaterial } from '@react-three/drei'
import * as THREE from 'three'

// Define custom shader material
const GradientMaterial = shaderMaterial(
  // Uniforms
  {
    uTime: 0,
    uColorA: new THREE.Color('#ff6b6b'),
    uColorB: new THREE.Color('#4ecdc4'),
    uFrequency: 2.0,
  },
  // Vertex shader
  /* glsl */ `
    varying vec2 vUv;
    varying vec3 vPosition;

    uniform float uTime;
    uniform float uFrequency;

    void main() {
      vUv = uv;
      vPosition = position;

      // Animated displacement
      vec3 pos = position;
      pos.z += sin(pos.x * uFrequency + uTime) * 0.1;
      pos.z += sin(pos.y * uFrequency + uTime * 0.5) * 0.1;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  // Fragment shader
  /* glsl */ `
    uniform float uTime;
    uniform vec3 uColorA;
    uniform vec3 uColorB;

    varying vec2 vUv;
    varying vec3 vPosition;

    void main() {
      // Animated gradient
      float mixFactor = sin(vUv.x * 3.14159 + uTime) * 0.5 + 0.5;
      vec3 color = mix(uColorA, uColorB, mixFactor);

      // Add some variation
      color += sin(vUv.y * 10.0 + uTime * 2.0) * 0.05;

      gl_FragColor = vec4(color, 1.0);
    }
  `
)

// Extend Three.js
extend({ GradientMaterial })

// TypeScript declaration
declare module '@react-three/fiber' {
  interface ThreeElements {
    gradientMaterial: Object3DNode<
      InstanceType<typeof GradientMaterial>,
      typeof GradientMaterial
    >
  }
}

// Component using custom material
export function GradientPlane() {
  const materialRef = useRef<InstanceType<typeof GradientMaterial>>(null)

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uTime = state.clock.elapsedTime
    }
  })

  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]}>
      <planeGeometry args={[10, 10, 64, 64]} />
      <gradientMaterial ref={materialRef} side={THREE.DoubleSide} />
    </mesh>
  )
}
```

### Matcap Material (No Lighting Needed)

```typescript
import { useMatcapTexture, Center } from '@react-three/drei'

export function MatcapModel() {
  // Many matcap IDs available: https://github.com/nidorx/matcaps
  const [matcap] = useMatcapTexture('CB4E88_F99AD6_F384C3_ED75B9', 256)

  return (
    <Center>
      <mesh>
        <torusKnotGeometry args={[1, 0.3, 128, 32]} />
        <meshMatcapMaterial matcap={matcap} />
      </mesh>
    </Center>
  )
}
```

---

## 5. Lighting

### Complete Lighting Setup

```typescript
import { useRef } from 'react'
import { useHelper } from '@react-three/drei'
import * as THREE from 'three'

interface LightingProps {
  debug?: boolean
}

export function Lighting({ debug = false }: LightingProps) {
  const directionalRef = useRef<THREE.DirectionalLight>(null)
  const spotRef = useRef<THREE.SpotLight>(null)
  const pointRef = useRef<THREE.PointLight>(null)

  // Debug helpers
  useHelper(debug && directionalRef, THREE.DirectionalLightHelper, 1, '#ffff00')
  useHelper(debug && spotRef, THREE.SpotLightHelper, '#00ff00')
  useHelper(debug && pointRef, THREE.PointLightHelper, 0.5, '#ff0000')

  return (
    <>
      {/* Ambient - base illumination */}
      <ambientLight intensity={0.2} color="#ffffff" />

      {/* Directional - sun-like parallel rays */}
      <directionalLight
        ref={directionalRef}
        position={[10, 10, 5]}
        intensity={1.5}
        color="#ffffff"
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-near={0.1}
        shadow-camera-far={50}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
        shadow-bias={-0.0001}
      />

      {/* Spot - cone of light */}
      <spotLight
        ref={spotRef}
        position={[-5, 8, 0]}
        angle={Math.PI / 6}
        penumbra={0.5}
        intensity={2}
        color="#ff9966"
        castShadow
        shadow-mapSize={[1024, 1024]}
        shadow-bias={-0.0001}
      />

      {/* Point - omnidirectional */}
      <pointLight
        ref={pointRef}
        position={[0, 3, -5]}
        intensity={1}
        color="#6699ff"
        distance={20}
        decay={2}
      />

      {/* Hemisphere - sky/ground gradient */}
      <hemisphereLight
        args={['#87ceeb', '#3d3d3d', 0.5]}
        position={[0, 50, 0]}
      />
    </>
  )
}
```

### Environment Lighting

```typescript
import { Environment, Sky, Stars, Cloud, Lightformer } from '@react-three/drei'

// HDRI environment
export function HDRIEnvironment() {
  return (
    <Environment
      files="/hdri/warehouse.hdr"
      background
      blur={0.5}
      resolution={256}
    />
  )
}

// Preset environments
export function PresetEnvironment() {
  return (
    <Environment
      preset="sunset" // 'apartment', 'city', 'dawn', 'forest', 'lobby', 'night', 'park', 'studio', 'sunset', 'warehouse'
      background
      blur={0}
    />
  )
}

// Custom studio lighting
export function StudioEnvironment() {
  return (
    <Environment resolution={256}>
      <group rotation={[-Math.PI / 3, 0, 1]}>
        <Lightformer
          form="circle"
          intensity={100}
          rotation-x={Math.PI / 2}
          position={[0, 5, -9]}
          scale={2}
        />
        <Lightformer
          form="circle"
          intensity={2}
          rotation-y={Math.PI / 2}
          position={[-5, 1, -1]}
          scale={2}
        />
        <Lightformer
          form="ring"
          color="#4060ff"
          intensity={10}
          onUpdate={(self) => self.lookAt(0, 0, 0)}
          position={[10, 10, 0]}
          scale={10}
        />
      </group>
    </Environment>
  )
}

// Sky and atmosphere
export function Atmosphere() {
  return (
    <>
      <Sky
        distance={450000}
        sunPosition={[0, 1, 0]}
        inclination={0.6}
        azimuth={0.25}
        mieCoefficient={0.005}
        rayleigh={0.5}
      />
      <Stars
        radius={100}
        depth={50}
        count={5000}
        factor={4}
        saturation={0}
        fade
        speed={1}
      />
      <Cloud
        position={[0, 10, 0]}
        opacity={0.5}
        speed={0.4}
        width={10}
        depth={1.5}
        segments={20}
      />
    </>
  )
}
```

### Contact Shadows

```typescript
import { ContactShadows, AccumulativeShadows, RandomizedLight } from '@react-three/drei'

// Simple contact shadows (baked, fast)
export function SimpleContactShadow() {
  return (
    <ContactShadows
      position={[0, -0.01, 0]}
      opacity={0.5}
      scale={10}
      blur={2}
      far={4}
      resolution={256}
      color="#000000"
    />
  )
}

// Accumulative shadows (higher quality, computed once)
export function QualityShadow() {
  return (
    <AccumulativeShadows
      temporal
      frames={100}
      position={[0, -0.01, 0]}
      scale={10}
      color="#316d39"
      opacity={0.8}
    >
      <RandomizedLight
        amount={8}
        radius={4}
        ambient={0.5}
        intensity={1}
        position={[5, 5, -10]}
        bias={0.001}
      />
    </AccumulativeShadows>
  )
}
```

---

## 6. Animation

### useFrame Animation

```typescript
import { useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

export function AnimatedMesh() {
  const meshRef = useRef<THREE.Mesh>(null)
  const { clock, pointer } = useThree()

  useFrame((state, delta) => {
    if (!meshRef.current) return

    // Time-based animation
    const t = state.clock.elapsedTime

    // Rotation
    meshRef.current.rotation.x = t * 0.5
    meshRef.current.rotation.y = t * 0.3

    // Position oscillation
    meshRef.current.position.y = Math.sin(t * 2) * 0.5

    // Scale pulse
    const scale = 1 + Math.sin(t * 3) * 0.1
    meshRef.current.scale.setScalar(scale)

    // Follow mouse (smoothed)
    meshRef.current.position.x = THREE.MathUtils.lerp(
      meshRef.current.position.x,
      state.pointer.x * 2,
      delta * 3
    )
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="#ff6b6b" />
    </mesh>
  )
}
```

### Spring Animation with @react-spring/three

```typescript
import { useRef, useState } from 'react'
import { useSpring, animated, config } from '@react-spring/three'
import * as THREE from 'three'

export function SpringBox() {
  const [active, setActive] = useState(false)

  const { scale, rotation, color } = useSpring({
    scale: active ? 1.5 : 1,
    rotation: active ? [0, Math.PI, 0] : [0, 0, 0],
    color: active ? '#ff6b6b' : '#4ecdc4',
    config: config.wobbly,
  })

  return (
    <animated.mesh
      scale={scale}
      rotation={rotation as any}
      onClick={() => setActive(!active)}
    >
      <boxGeometry />
      <animated.meshStandardMaterial color={color} />
    </animated.mesh>
  )
}

// Sequential spring animation
export function SequentialAnimation() {
  const [step, setStep] = useState(0)

  const { position, rotation, scale } = useSpring({
    position: step === 0 ? [0, 0, 0] : step === 1 ? [2, 0, 0] : [2, 2, 0],
    rotation: step === 0 ? [0, 0, 0] : step === 1 ? [0, Math.PI, 0] : [Math.PI, Math.PI, 0],
    scale: step === 0 ? 1 : step === 1 ? 1.5 : 0.5,
    config: { mass: 1, tension: 180, friction: 12 },
  })

  return (
    <animated.mesh
      position={position as any}
      rotation={rotation as any}
      scale={scale}
      onClick={() => setStep((s) => (s + 1) % 3)}
    >
      <boxGeometry />
      <meshStandardMaterial color="#88ccff" />
    </animated.mesh>
  )
}
```

### Scroll-Linked Animation

```typescript
import { useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useScroll, ScrollControls, Scroll } from '@react-three/drei'
import * as THREE from 'three'

// Scroll-controlled experience
export function ScrollExperience() {
  return (
    <ScrollControls pages={3} damping={0.25}>
      <Scroll>
        <ScrollScene />
      </Scroll>
      <Scroll html>
        <div className="w-screen">
          <section className="h-screen flex items-center justify-center">
            <h1 className="text-6xl text-white">Section 1</h1>
          </section>
          <section className="h-screen flex items-center justify-center">
            <h1 className="text-6xl text-white">Section 2</h1>
          </section>
          <section className="h-screen flex items-center justify-center">
            <h1 className="text-6xl text-white">Section 3</h1>
          </section>
        </div>
      </Scroll>
    </ScrollControls>
  )
}

function ScrollScene() {
  const groupRef = useRef<THREE.Group>(null)
  const scroll = useScroll()

  useFrame(() => {
    if (!groupRef.current) return

    // scroll.offset is 0-1 based on scroll position
    const offset = scroll.offset

    // Rotate based on scroll
    groupRef.current.rotation.y = offset * Math.PI * 2

    // Move camera or objects based on scroll
    groupRef.current.position.y = -offset * 5

    // Use scroll.range for section-specific animations
    const section1 = scroll.range(0, 1 / 3) // 0-1 for first third
    const section2 = scroll.range(1 / 3, 1 / 3) // 0-1 for second third
    const section3 = scroll.range(2 / 3, 1 / 3) // 0-1 for final third

    // Scale based on section
    groupRef.current.scale.setScalar(1 + section2 * 0.5)
  })

  return (
    <group ref={groupRef}>
      <mesh position={[0, 0, 0]}>
        <boxGeometry />
        <meshStandardMaterial color="#ff6b6b" />
      </mesh>
      <mesh position={[0, -3, 0]}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial color="#4ecdc4" />
      </mesh>
      <mesh position={[0, -6, 0]}>
        <torusGeometry args={[0.5, 0.2, 32, 64]} />
        <meshStandardMaterial color="#ffd93d" />
      </mesh>
    </group>
  )
}
```

### Camera Animation

```typescript
import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { CameraControls, PerspectiveCamera } from '@react-three/drei'
import * as THREE from 'three'

// Animated camera with CameraControls
export function AnimatedCamera() {
  const controlsRef = useRef<CameraControls>(null)

  const moveTo = async (position: [number, number, number], target: [number, number, number]) => {
    if (!controlsRef.current) return
    await controlsRef.current.setLookAt(
      position[0], position[1], position[2],
      target[0], target[1], target[2],
      true // smooth animation
    )
  }

  useEffect(() => {
    // Initial camera animation
    moveTo([5, 3, 5], [0, 0, 0])
  }, [])

  return (
    <>
      <PerspectiveCamera makeDefault position={[10, 10, 10]} />
      <CameraControls
        ref={controlsRef}
        minDistance={2}
        maxDistance={20}
        dollySpeed={0.5}
        truckSpeed={0.5}
      />
    </>
  )
}

// Manual camera animation
export function ManualCameraAnimation() {
  const { camera } = useThree()
  const targetPosition = useRef(new THREE.Vector3(5, 3, 5))
  const targetLookAt = useRef(new THREE.Vector3(0, 0, 0))

  useFrame((state, delta) => {
    // Smooth camera movement
    camera.position.lerp(targetPosition.current, delta * 2)

    // Create a temporary vector for lookAt
    const currentLookAt = new THREE.Vector3()
    camera.getWorldDirection(currentLookAt)
    currentLookAt.add(camera.position)
    currentLookAt.lerp(targetLookAt.current, delta * 2)
    camera.lookAt(currentLookAt)
  })

  return null
}
```

---

## 7. Interaction

### Raycasting and Events

```typescript
import { useState, useRef } from 'react'
import { ThreeEvent } from '@react-three/fiber'
import * as THREE from 'three'

export function InteractiveMesh() {
  const [hovered, setHovered] = useState(false)
  const [clicked, setClicked] = useState(false)
  const meshRef = useRef<THREE.Mesh>(null)

  const handlePointerOver = (e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation()
    setHovered(true)
    document.body.style.cursor = 'pointer'
  }

  const handlePointerOut = (e: ThreeEvent<PointerEvent>) => {
    setHovered(false)
    document.body.style.cursor = 'default'
  }

  const handleClick = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation()
    setClicked(!clicked)

    // Access intersection data
    console.log('Hit point:', e.point)
    console.log('Face normal:', e.face?.normal)
    console.log('Distance:', e.distance)
    console.log('UV:', e.uv)
  }

  return (
    <mesh
      ref={meshRef}
      scale={clicked ? 1.5 : 1}
      onPointerOver={handlePointerOver}
      onPointerOut={handlePointerOut}
      onClick={handleClick}
      onPointerMove={(e) => {
        // Track pointer position on surface
        if (meshRef.current) {
          meshRef.current.material.color.setHSL(e.uv!.x, 0.7, 0.5)
        }
      }}
    >
      <boxGeometry />
      <meshStandardMaterial color={hovered ? '#ff6b6b' : '#4ecdc4'} />
    </mesh>
  )
}
```

### Drag Controls

```typescript
import { useRef, useState } from 'react'
import { useDrag } from '@use-gesture/react'
import { useThree } from '@react-three/fiber'
import { useSpring, animated } from '@react-spring/three'
import * as THREE from 'three'

export function DraggableMesh() {
  const meshRef = useRef<THREE.Mesh>(null)
  const [isDragging, setIsDragging] = useState(false)
  const { size, viewport } = useThree()
  const aspect = size.width / viewport.width

  const [spring, api] = useSpring(() => ({
    position: [0, 0, 0],
    scale: 1,
    config: { mass: 1, friction: 40, tension: 800 },
  }))

  const bind = useDrag(
    ({ active, movement: [x, y], memo = spring.position.get() }) => {
      setIsDragging(active)

      api.start({
        position: [memo[0] + x / aspect, memo[1] - y / aspect, 0],
        scale: active ? 1.2 : 1,
      })

      return memo
    },
    { pointer: { touch: true } }
  )

  return (
    <animated.mesh
      ref={meshRef}
      {...(bind() as any)}
      position={spring.position as any}
      scale={spring.scale}
    >
      <boxGeometry />
      <meshStandardMaterial color={isDragging ? '#ff6b6b' : '#4ecdc4'} />
    </animated.mesh>
  )
}
```

### Drei Drag Controls

```typescript
import { useRef } from 'react'
import { DragControls, PivotControls, TransformControls } from '@react-three/drei'
import * as THREE from 'three'

export function DragControlsExample() {
  const groupRef = useRef<THREE.Group>(null)

  return (
    <DragControls
      autoTransform
      onDragStart={() => console.log('Drag started')}
      onDrag={(localMatrix, deltaLocalMatrix, worldMatrix, deltaWorldMatrix) => {
        console.log('Dragging', localMatrix)
      }}
      onDragEnd={() => console.log('Drag ended')}
    >
      <mesh>
        <boxGeometry />
        <meshStandardMaterial color="#ff6b6b" />
      </mesh>
    </DragControls>
  )
}

// Gizmo-style controls
export function PivotControlsExample() {
  return (
    <PivotControls
      anchor={[0, 0, 0]}
      depthTest={false}
      lineWidth={2}
      axisColors={['#ff0000', '#00ff00', '#0000ff']}
      scale={1}
    >
      <mesh>
        <boxGeometry />
        <meshStandardMaterial color="#4ecdc4" />
      </mesh>
    </PivotControls>
  )
}

// Transform controls (like in 3D editors)
export function TransformControlsExample() {
  const meshRef = useRef<THREE.Mesh>(null)

  return (
    <>
      <mesh ref={meshRef}>
        <boxGeometry />
        <meshStandardMaterial color="#ffd93d" />
      </mesh>
      <TransformControls
        object={meshRef.current!}
        mode="translate" // 'translate', 'rotate', 'scale'
      />
    </>
  )
}
```

---

## 8. Shaders

### Basic Shader Material

```typescript
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

const vertexShader = /* glsl */ `
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vPosition;

  void main() {
    vUv = uv;
    vNormal = normalize(normalMatrix * normal);
    vPosition = position;

    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`

const fragmentShader = /* glsl */ `
  uniform float uTime;
  uniform vec3 uColor;
  uniform sampler2D uTexture;

  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vPosition;

  void main() {
    // Fresnel effect
    vec3 viewDirection = normalize(cameraPosition - vPosition);
    float fresnel = pow(1.0 - dot(viewDirection, vNormal), 3.0);

    // Animated pattern
    float pattern = sin(vUv.x * 10.0 + uTime) * sin(vUv.y * 10.0 + uTime);

    vec3 color = uColor + fresnel * 0.5;
    color += pattern * 0.1;

    gl_FragColor = vec4(color, 1.0);
  }
`

export function ShaderMesh() {
  const meshRef = useRef<THREE.Mesh>(null)
  const uniformsRef = useRef({
    uTime: { value: 0 },
    uColor: { value: new THREE.Color('#4ecdc4') },
    uTexture: { value: null },
  })

  useFrame((state) => {
    uniformsRef.current.uTime.value = state.clock.elapsedTime
  })

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[1, 64, 64]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniformsRef.current}
      />
    </mesh>
  )
}
```

### Noise Displacement Shader

```typescript
import { useRef } from 'react'
import { useFrame, extend, Object3DNode } from '@react-three/fiber'
import { shaderMaterial } from '@react-three/drei'
import * as THREE from 'three'

// Simplex noise function (include in shader)
const noiseGLSL = /* glsl */ `
  vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec4 permute(vec4 x) { return mod289(((x*34.0)+1.0)*x); }
  vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

  float snoise(vec3 v) {
    const vec2 C = vec2(1.0/6.0, 1.0/3.0);
    const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);

    vec3 i  = floor(v + dot(v, C.yyy));
    vec3 x0 = v - i + dot(i, C.xxx);

    vec3 g = step(x0.yzx, x0.xyz);
    vec3 l = 1.0 - g;
    vec3 i1 = min(g.xyz, l.zxy);
    vec3 i2 = max(g.xyz, l.zxy);

    vec3 x1 = x0 - i1 + C.xxx;
    vec3 x2 = x0 - i2 + C.yyy;
    vec3 x3 = x0 - D.yyy;

    i = mod289(i);
    vec4 p = permute(permute(permute(
              i.z + vec4(0.0, i1.z, i2.z, 1.0))
            + i.y + vec4(0.0, i1.y, i2.y, 1.0))
            + i.x + vec4(0.0, i1.x, i2.x, 1.0));

    float n_ = 0.142857142857;
    vec3 ns = n_ * D.wyz - D.xzx;

    vec4 j = p - 49.0 * floor(p * ns.z * ns.z);

    vec4 x_ = floor(j * ns.z);
    vec4 y_ = floor(j - 7.0 * x_);

    vec4 x = x_ *ns.x + ns.yyyy;
    vec4 y = y_ *ns.x + ns.yyyy;
    vec4 h = 1.0 - abs(x) - abs(y);

    vec4 b0 = vec4(x.xy, y.xy);
    vec4 b1 = vec4(x.zw, y.zw);

    vec4 s0 = floor(b0)*2.0 + 1.0;
    vec4 s1 = floor(b1)*2.0 + 1.0;
    vec4 sh = -step(h, vec4(0.0));

    vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy;
    vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww;

    vec3 p0 = vec3(a0.xy, h.x);
    vec3 p1 = vec3(a0.zw, h.y);
    vec3 p2 = vec3(a1.xy, h.z);
    vec3 p3 = vec3(a1.zw, h.w);

    vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
    p0 *= norm.x;
    p1 *= norm.y;
    p2 *= norm.z;
    p3 *= norm.w;

    vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
    m = m * m;
    return 42.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
  }
`

const NoiseMaterial = shaderMaterial(
  {
    uTime: 0,
    uNoiseScale: 2.0,
    uNoiseStrength: 0.3,
    uColorA: new THREE.Color('#1a1a2e'),
    uColorB: new THREE.Color('#16213e'),
    uColorC: new THREE.Color('#0f3460'),
  },
  // Vertex shader
  noiseGLSL + /* glsl */ `
    uniform float uTime;
    uniform float uNoiseScale;
    uniform float uNoiseStrength;

    varying vec2 vUv;
    varying float vElevation;

    void main() {
      vUv = uv;

      // Calculate noise-based displacement
      float elevation = snoise(vec3(position.xy * uNoiseScale, uTime * 0.3)) * uNoiseStrength;
      vElevation = elevation;

      vec3 newPosition = position + normal * elevation;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
    }
  `,
  // Fragment shader
  /* glsl */ `
    uniform vec3 uColorA;
    uniform vec3 uColorB;
    uniform vec3 uColorC;

    varying vec2 vUv;
    varying float vElevation;

    void main() {
      // Create gradient based on elevation
      float mixA = smoothstep(-0.3, 0.0, vElevation);
      float mixB = smoothstep(0.0, 0.3, vElevation);

      vec3 color = mix(uColorA, uColorB, mixA);
      color = mix(color, uColorC, mixB);

      gl_FragColor = vec4(color, 1.0);
    }
  `
)

extend({ NoiseMaterial })

declare module '@react-three/fiber' {
  interface ThreeElements {
    noiseMaterial: Object3DNode<InstanceType<typeof NoiseMaterial>, typeof NoiseMaterial>
  }
}

export function NoiseSphere() {
  const materialRef = useRef<InstanceType<typeof NoiseMaterial>>(null)

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uTime = state.clock.elapsedTime
    }
  })

  return (
    <mesh>
      <icosahedronGeometry args={[2, 64]} />
      <noiseMaterial ref={materialRef} />
    </mesh>
  )
}
```

### GLSL Shader with Texture

```typescript
import { useRef, useEffect } from 'react'
import { useFrame, useLoader } from '@react-three/fiber'
import * as THREE from 'three'

const vertexShader = /* glsl */ `
  varying vec2 vUv;

  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`

const fragmentShader = /* glsl */ `
  uniform float uTime;
  uniform sampler2D uTexture;
  uniform vec2 uMouse;

  varying vec2 vUv;

  void main() {
    // Distortion based on mouse position
    vec2 distortion = (uMouse - 0.5) * 0.1;
    float dist = distance(vUv, uMouse);
    distortion *= smoothstep(0.5, 0.0, dist);

    // Wave distortion
    vec2 waveUv = vUv;
    waveUv.x += sin(vUv.y * 20.0 + uTime * 2.0) * 0.01;
    waveUv.y += sin(vUv.x * 20.0 + uTime * 2.0) * 0.01;

    vec4 color = texture2D(uTexture, waveUv + distortion);

    gl_FragColor = color;
  }
`

export function TextureShader() {
  const meshRef = useRef<THREE.Mesh>(null)
  const texture = useLoader(THREE.TextureLoader, '/textures/image.jpg')

  const uniforms = useRef({
    uTime: { value: 0 },
    uTexture: { value: texture },
    uMouse: { value: new THREE.Vector2(0.5, 0.5) },
  })

  useFrame((state) => {
    uniforms.current.uTime.value = state.clock.elapsedTime
    uniforms.current.uMouse.value.set(
      (state.pointer.x + 1) / 2,
      (state.pointer.y + 1) / 2
    )
  })

  return (
    <mesh ref={meshRef}>
      <planeGeometry args={[4, 3, 32, 32]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms.current}
      />
    </mesh>
  )
}
```

---

## 9. Post-Processing

### Basic Post-Processing Setup

```typescript
import { EffectComposer, Bloom, ChromaticAberration, Vignette, Noise, DepthOfField } from '@react-three/postprocessing'
import { BlendFunction, KernelSize } from 'postprocessing'

export function PostProcessing() {
  return (
    <EffectComposer>
      <Bloom
        intensity={1}
        luminanceThreshold={0.9}
        luminanceSmoothing={0.025}
        kernelSize={KernelSize.LARGE}
        mipmapBlur
      />
      <ChromaticAberration
        blendFunction={BlendFunction.NORMAL}
        offset={[0.002, 0.002]}
        radialModulation={true}
        modulationOffset={0.5}
      />
      <Vignette
        offset={0.3}
        darkness={0.9}
        blendFunction={BlendFunction.NORMAL}
      />
      <Noise
        opacity={0.02}
        blendFunction={BlendFunction.OVERLAY}
      />
    </EffectComposer>
  )
}
```

### Depth of Field

```typescript
import { useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { EffectComposer, DepthOfField } from '@react-three/postprocessing'
import * as THREE from 'three'

export function DOFPostProcessing() {
  const dofRef = useRef<any>(null)
  const { camera } = useThree()

  useFrame((state) => {
    if (!dofRef.current) return

    // Dynamic focus based on mouse or target
    const focusDistance = 5 + Math.sin(state.clock.elapsedTime) * 2
    dofRef.current.circleOfConfusionMaterial.uniforms.focusDistance.value = focusDistance
  })

  return (
    <EffectComposer>
      <DepthOfField
        ref={dofRef}
        focusDistance={0.02}
        focalLength={0.02}
        bokehScale={3}
        height={480}
      />
    </EffectComposer>
  )
}
```

### Custom Effect

```typescript
import { forwardRef, useMemo } from 'react'
import { Effect, BlendFunction } from 'postprocessing'
import { Uniform } from 'three'
import { EffectComposer } from '@react-three/postprocessing'
import { useFrame } from '@react-three/fiber'

const fragmentShader = /* glsl */ `
  uniform float uTime;
  uniform float uIntensity;

  void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
    // Scanline effect
    float scanline = sin(uv.y * 800.0 + uTime * 10.0) * 0.04 * uIntensity;

    // RGB shift
    float shift = 0.003 * uIntensity;
    vec4 r = texture2D(inputBuffer, uv + vec2(shift, 0.0));
    vec4 g = texture2D(inputBuffer, uv);
    vec4 b = texture2D(inputBuffer, uv - vec2(shift, 0.0));

    vec4 color = vec4(r.r, g.g, b.b, inputColor.a);
    color.rgb += scanline;

    outputColor = color;
  }
`

class GlitchEffectImpl extends Effect {
  constructor({ intensity = 1 } = {}) {
    super('GlitchEffect', fragmentShader, {
      blendFunction: BlendFunction.NORMAL,
      uniforms: new Map([
        ['uTime', new Uniform(0)],
        ['uIntensity', new Uniform(intensity)],
      ]),
    })
  }

  update(renderer: any, inputBuffer: any, deltaTime: number) {
    this.uniforms.get('uTime')!.value += deltaTime
  }
}

export const GlitchEffect = forwardRef<GlitchEffectImpl, { intensity?: number }>(
  ({ intensity = 1 }, ref) => {
    const effect = useMemo(() => new GlitchEffectImpl({ intensity }), [intensity])
    return <primitive ref={ref} object={effect} />
  }
)

// Usage
export function CustomPostProcessing() {
  return (
    <EffectComposer>
      <GlitchEffect intensity={0.5} />
    </EffectComposer>
  )
}
```

### Selective Bloom

```typescript
import { useRef } from 'react'
import { EffectComposer, Bloom, SelectiveBloom } from '@react-three/postprocessing'
import { Selection, Select } from '@react-three/postprocessing'
import * as THREE from 'three'

export function SelectiveBloomScene() {
  const lightRef = useRef<THREE.PointLight>(null)

  return (
    <>
      <Selection>
        <EffectComposer>
          <SelectiveBloom
            lights={[lightRef]}
            intensity={2}
            luminanceThreshold={0}
            luminanceSmoothing={0.9}
            mipmapBlur
          />
        </EffectComposer>

        {/* This mesh will bloom */}
        <Select enabled>
          <mesh position={[0, 0, 0]}>
            <sphereGeometry args={[1, 32, 32]} />
            <meshStandardMaterial
              emissive="#ff6b6b"
              emissiveIntensity={2}
              color="#ff6b6b"
            />
          </mesh>
        </Select>

        {/* This mesh will NOT bloom */}
        <mesh position={[3, 0, 0]}>
          <boxGeometry />
          <meshStandardMaterial color="#4ecdc4" />
        </mesh>
      </Selection>

      <pointLight ref={lightRef} position={[0, 5, 0]} intensity={1} />
    </>
  )
}
```

---

## 10. Performance

### Instancing for Many Objects

```typescript
import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { Instance, Instances } from '@react-three/drei'
import * as THREE from 'three'

// Drei Instances (easier API)
export function DreiInstances({ count = 1000 }) {
  const data = useMemo(() => {
    return Array.from({ length: count }, () => ({
      position: [
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20,
      ] as [number, number, number],
      rotation: [
        Math.random() * Math.PI,
        Math.random() * Math.PI,
        Math.random() * Math.PI,
      ] as [number, number, number],
      scale: 0.2 + Math.random() * 0.3,
    }))
  }, [count])

  return (
    <Instances limit={count} castShadow receiveShadow>
      <boxGeometry />
      <meshStandardMaterial />
      {data.map((props, i) => (
        <Instance key={i} {...props} />
      ))}
    </Instances>
  )
}

// Animated instances
function AnimatedInstance({ position, speed }: { position: [number, number, number]; speed: number }) {
  const ref = useRef<THREE.InstancedMesh>(null)

  useFrame((state) => {
    if (!ref.current) return
    ref.current.rotation.x = state.clock.elapsedTime * speed
    ref.current.rotation.y = state.clock.elapsedTime * speed * 0.5
  })

  return <Instance ref={ref} position={position} />
}
```

### Level of Detail (LOD)

```typescript
import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { Detailed, useGLTF } from '@react-three/drei'
import * as THREE from 'three'

// Built-in LOD with Detailed
export function LODModel() {
  return (
    <Detailed distances={[0, 10, 20, 50]}>
      {/* High detail - closest */}
      <mesh>
        <sphereGeometry args={[1, 64, 64]} />
        <meshStandardMaterial color="#ff6b6b" />
      </mesh>
      {/* Medium detail */}
      <mesh>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial color="#ff6b6b" />
      </mesh>
      {/* Low detail */}
      <mesh>
        <sphereGeometry args={[1, 16, 16]} />
        <meshStandardMaterial color="#ff6b6b" />
      </mesh>
      {/* Lowest detail - farthest */}
      <mesh>
        <sphereGeometry args={[1, 8, 8]} />
        <meshStandardMaterial color="#ff6b6b" />
      </mesh>
    </Detailed>
  )
}

// Manual LOD with THREE.LOD
export function ManualLOD() {
  const lodRef = useRef<THREE.LOD>(null)

  const levels = useMemo(() => [
    { geometry: new THREE.SphereGeometry(1, 64, 64), distance: 0 },
    { geometry: new THREE.SphereGeometry(1, 32, 32), distance: 10 },
    { geometry: new THREE.SphereGeometry(1, 16, 16), distance: 20 },
    { geometry: new THREE.SphereGeometry(1, 8, 8), distance: 50 },
  ], [])

  return (
    <lod ref={lodRef}>
      {levels.map(({ geometry, distance }, i) => (
        <mesh key={i} geometry={geometry}>
          <meshStandardMaterial color="#4ecdc4" />
        </mesh>
      ))}
    </lod>
  )
}
```

### Disposal and Memory Management

```typescript
import { useEffect, useRef } from 'react'
import { useThree } from '@react-three/fiber'
import * as THREE from 'three'

// Manual cleanup hook
export function useDisposable<T extends THREE.Object3D>(object: T | null) {
  useEffect(() => {
    return () => {
      if (!object) return

      object.traverse((child) => {
        if ((child as THREE.Mesh).geometry) {
          (child as THREE.Mesh).geometry.dispose()
        }
        if ((child as THREE.Mesh).material) {
          const material = (child as THREE.Mesh).material
          if (Array.isArray(material)) {
            material.forEach((m) => disposeMaterial(m))
          } else {
            disposeMaterial(material)
          }
        }
      })
    }
  }, [object])
}

function disposeMaterial(material: THREE.Material) {
  material.dispose()

  // Dispose textures
  Object.keys(material).forEach((key) => {
    const value = (material as any)[key]
    if (value instanceof THREE.Texture) {
      value.dispose()
    }
  })
}

// Component with cleanup
export function DisposableModel({ url }: { url: string }) {
  const groupRef = useRef<THREE.Group>(null)

  useDisposable(groupRef.current)

  return (
    <group ref={groupRef}>
      {/* Model content */}
    </group>
  )
}

// Texture disposal
export function useDisposableTexture(texture: THREE.Texture | null) {
  useEffect(() => {
    return () => {
      texture?.dispose()
    }
  }, [texture])
}
```

### Performance Monitoring

```typescript
import { useRef, useState, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Html, PerformanceMonitor } from '@react-three/drei'

// Drei PerformanceMonitor (adaptive quality)
export function AdaptiveScene({ children }: { children: React.ReactNode }) {
  const [dpr, setDpr] = useState(1.5)

  return (
    <>
      <PerformanceMonitor
        onIncline={() => setDpr(2)}
        onDecline={() => setDpr(1)}
        flipflops={3}
        onFallback={() => setDpr(0.5)}
      >
        {children}
      </PerformanceMonitor>
    </>
  )
}

// Custom stats display
export function Stats() {
  const [stats, setStats] = useState({ fps: 0, memory: 0 })
  const frameCount = useRef(0)
  const lastTime = useRef(performance.now())

  useFrame(() => {
    frameCount.current++
    const now = performance.now()

    if (now - lastTime.current >= 1000) {
      setStats({
        fps: frameCount.current,
        memory: (performance as any).memory?.usedJSHeapSize / 1024 / 1024 || 0,
      })
      frameCount.current = 0
      lastTime.current = now
    }
  })

  return (
    <Html position={[-5, 3, 0]}>
      <div className="bg-black/50 p-2 text-white text-xs font-mono">
        <div>FPS: {stats.fps}</div>
        <div>Memory: {stats.memory.toFixed(1)} MB</div>
      </div>
    </Html>
  )
}
```

### Frustum Culling and Bounding

```typescript
import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Bounds, useBounds } from '@react-three/drei'
import * as THREE from 'three'

// Auto bounds fitting
export function BoundedScene({ children }: { children: React.ReactNode }) {
  return (
    <Bounds fit clip observe margin={1.2}>
      {children}
    </Bounds>
  )
}

// Manual frustum culling
export function FrustumCulledObjects({ positions }: { positions: THREE.Vector3[] }) {
  const groupRef = useRef<THREE.Group>(null)
  const { camera } = useThree()
  const frustum = useRef(new THREE.Frustum())
  const matrix = useRef(new THREE.Matrix4())

  useFrame(() => {
    if (!groupRef.current) return

    // Update frustum
    matrix.current.multiplyMatrices(
      camera.projectionMatrix,
      camera.matrixWorldInverse
    )
    frustum.current.setFromProjectionMatrix(matrix.current)

    // Check each child
    groupRef.current.children.forEach((child) => {
      const mesh = child as THREE.Mesh
      if (mesh.geometry.boundingSphere) {
        mesh.visible = frustum.current.intersectsSphere(
          mesh.geometry.boundingSphere.clone().applyMatrix4(mesh.matrixWorld)
        )
      }
    })
  })

  return (
    <group ref={groupRef}>
      {positions.map((pos, i) => (
        <mesh key={i} position={pos}>
          <boxGeometry />
          <meshStandardMaterial />
        </mesh>
      ))}
    </group>
  )
}
```

---

## 11. Drei Utilities

### Html Overlay

```typescript
import { Html, Billboard } from '@react-three/drei'
import { useRef, useState } from 'react'
import * as THREE from 'three'

export function HtmlLabel() {
  const [hovered, setHovered] = useState(false)

  return (
    <group position={[0, 2, 0]}>
      <mesh
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial color="#ff6b6b" />
      </mesh>

      <Html
        position={[0, 1.5, 0]}
        center
        distanceFactor={10} // Scale with distance
        occlude // Hide when behind objects
        transform // Apply 3D transform
        sprite // Always face camera
      >
        <div
          className={`
            px-4 py-2 rounded-lg bg-white/90 backdrop-blur-sm
            text-black text-sm font-medium shadow-lg
            transition-opacity duration-200
            ${hovered ? 'opacity-100' : 'opacity-70'}
          `}
        >
          Interactive Sphere
        </div>
      </Html>
    </group>
  )
}

// Billboard (always faces camera)
export function BillboardExample() {
  return (
    <Billboard follow={true} lockX={false} lockY={false} lockZ={false}>
      <mesh>
        <planeGeometry args={[2, 1]} />
        <meshBasicMaterial color="#4ecdc4" side={THREE.DoubleSide} />
      </mesh>
    </Billboard>
  )
}
```

### 3D Text

```typescript
import { Text, Text3D, Center } from '@react-three/drei'
import { useRef } from 'react'
import * as THREE from 'three'

// Troika Text (2D text that faces camera)
export function TroikaText() {
  return (
    <Text
      position={[0, 2, 0]}
      fontSize={0.5}
      color="#ffffff"
      anchorX="center"
      anchorY="middle"
      font="/fonts/Inter-Bold.woff"
      maxWidth={10}
      lineHeight={1.2}
      letterSpacing={0.02}
      textAlign="center"
      outlineWidth={0.02}
      outlineColor="#000000"
    >
      Hello Three.js World!
    </Text>
  )
}

// 3D extruded text
export function Extruded3DText() {
  return (
    <Center>
      <Text3D
        font="/fonts/Inter_Bold.json"
        size={1}
        height={0.2}
        curveSegments={12}
        bevelEnabled
        bevelThickness={0.02}
        bevelSize={0.02}
        bevelOffset={0}
        bevelSegments={5}
      >
        3D TEXT
        <meshStandardMaterial color="#ff6b6b" metalness={0.8} roughness={0.2} />
      </Text3D>
    </Center>
  )
}
```

### Float and Animations

```typescript
import { Float, MeshWobbleMaterial, MeshDistortMaterial, Sparkles } from '@react-three/drei'

// Floating animation
export function FloatingObject() {
  return (
    <Float
      speed={2}
      rotationIntensity={1}
      floatIntensity={2}
      floatingRange={[-0.1, 0.1]}
    >
      <mesh>
        <torusKnotGeometry args={[1, 0.3, 128, 32]} />
        <meshStandardMaterial color="#4ecdc4" />
      </mesh>
    </Float>
  )
}

// Wobble material
export function WobblyMesh() {
  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <MeshWobbleMaterial
        color="#ff6b6b"
        factor={1} // Wobble strength
        speed={2} // Wobble speed
      />
    </mesh>
  )
}

// Distort material
export function DistortedMesh() {
  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <MeshDistortMaterial
        color="#ffd93d"
        distort={0.5} // Distortion strength
        speed={2} // Animation speed
        roughness={0.2}
      />
    </mesh>
  )
}

// Sparkles
export function SparkleEffect() {
  return (
    <Sparkles
      count={100}
      scale={[4, 4, 4]}
      size={2}
      speed={0.3}
      opacity={0.8}
      color="#ffffff"
    />
  )
}
```

### Image and Video

```typescript
import { Image, useVideoTexture, useTexture } from '@react-three/drei'
import * as THREE from 'three'

// Drei Image component
export function ImagePlane() {
  return (
    <Image
      url="/images/texture.jpg"
      position={[0, 0, 0]}
      scale={[4, 3]}
      transparent
      opacity={1}
      toneMapped={false}
    />
  )
}

// Video texture
export function VideoPlane() {
  const texture = useVideoTexture('/videos/background.mp4', {
    muted: true,
    loop: true,
    start: true,
  })

  return (
    <mesh>
      <planeGeometry args={[16, 9]} />
      <meshBasicMaterial map={texture} toneMapped={false} />
    </mesh>
  )
}

// Multiple textures
export function MultiTextured() {
  const [colorMap, normalMap, roughnessMap] = useTexture([
    '/textures/color.jpg',
    '/textures/normal.jpg',
    '/textures/roughness.jpg',
  ])

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        map={colorMap}
        normalMap={normalMap}
        roughnessMap={roughnessMap}
      />
    </mesh>
  )
}
```

### OrbitControls and Camera Helpers

```typescript
import { OrbitControls, MapControls, FlyControls, PointerLockControls, PresentationControls, CameraShake } from '@react-three/drei'
import { useRef } from 'react'

// Standard orbit controls
export function OrbitControlsExample() {
  return (
    <OrbitControls
      makeDefault
      enableDamping
      dampingFactor={0.05}
      minDistance={2}
      maxDistance={20}
      minPolarAngle={0}
      maxPolarAngle={Math.PI / 2}
      enablePan={false}
      autoRotate
      autoRotateSpeed={0.5}
    />
  )
}

// Presentation controls (drag to rotate object)
export function PresentationControlsExample({ children }: { children: React.ReactNode }) {
  return (
    <PresentationControls
      global
      config={{ mass: 2, tension: 500 }}
      snap={{ mass: 4, tension: 1500 }}
      rotation={[0, 0.3, 0]}
      polar={[-Math.PI / 3, Math.PI / 3]}
      azimuth={[-Math.PI / 1.4, Math.PI / 2]}
    >
      {children}
    </PresentationControls>
  )
}

// Camera shake
export function CameraShakeExample() {
  return (
    <CameraShake
      maxYaw={0.1}
      maxPitch={0.1}
      maxRoll={0.1}
      yawFrequency={0.1}
      pitchFrequency={0.1}
      rollFrequency={0.1}
      intensity={1}
      decayRate={0.65}
    />
  )
}
```

---

## Complete Scene Example

```typescript
'use client'

import { Suspense, useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import {
  Environment,
  OrbitControls,
  ContactShadows,
  Float,
  Text,
  PerspectiveCamera,
  useGLTF,
} from '@react-three/drei'
import { EffectComposer, Bloom, Vignette } from '@react-three/postprocessing'
import * as THREE from 'three'

function Model() {
  const groupRef = useRef<THREE.Group>(null)

  useFrame((state) => {
    if (!groupRef.current) return
    groupRef.current.rotation.y = state.clock.elapsedTime * 0.2
  })

  return (
    <group ref={groupRef}>
      <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
        <mesh castShadow>
          <torusKnotGeometry args={[0.8, 0.3, 128, 32]} />
          <meshStandardMaterial
            color="#ff6b6b"
            roughness={0.2}
            metalness={0.8}
            envMapIntensity={1}
          />
        </mesh>
      </Float>
    </group>
  )
}

function Scene() {
  return (
    <>
      <PerspectiveCamera makeDefault position={[0, 2, 5]} fov={45} />
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        minDistance={3}
        maxDistance={10}
      />

      <ambientLight intensity={0.2} />
      <directionalLight
        position={[5, 5, 5]}
        intensity={1}
        castShadow
        shadow-mapSize={[2048, 2048]}
      />

      <Model />

      <ContactShadows
        position={[0, -1.5, 0]}
        opacity={0.5}
        scale={10}
        blur={2}
        far={4}
      />

      <Environment preset="city" background blur={0.5} />

      <Text
        position={[0, 2.5, 0]}
        fontSize={0.3}
        color="#ffffff"
        anchorX="center"
      >
        React Three Fiber
      </Text>

      <EffectComposer>
        <Bloom
          intensity={0.5}
          luminanceThreshold={0.9}
          luminanceSmoothing={0.025}
        />
        <Vignette offset={0.3} darkness={0.5} />
      </EffectComposer>
    </>
  )
}

export default function Experience() {
  return (
    <div className="h-screen w-full">
      <Canvas
        shadows
        dpr={[1, 2]}
        gl={{
          antialias: true,
          outputColorSpace: THREE.SRGBColorSpace,
          toneMapping: THREE.ACESFilmicToneMapping,
        }}
      >
        <color attach="background" args={['#1a1a2e']} />
        <fog attach="fog" args={['#1a1a2e', 5, 20]} />
        <Suspense fallback={null}>
          <Scene />
        </Suspense>
      </Canvas>
    </div>
  )
}
```

---

## Best Practices Summary

1. **Always use Suspense** for loading states
2. **Preload assets** with `useGLTF.preload()` and `useTexture.preload()`
3. **Use instancing** for many similar objects (1000+ is fine)
4. **Implement LOD** for complex scenes
5. **Dispose resources** when components unmount
6. **Use `dpr={[1, 2]}`** to clamp device pixel ratio
7. **Minimize draw calls** by merging geometries where possible
8. **Use `frameloop="demand"`** for static scenes
9. **Profile with `r3f-perf`** during development
10. **Prefer Drei utilities** over manual implementations
