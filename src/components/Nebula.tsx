import { useRef, useState, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Html, Stars, Sparkles, OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import { planets, type Planet } from '../data/planets';

type LayoutItem = { planet: Planet; basePos: [number, number, number] };

// ===== 连线层:把相邻星球用细线连成星座网络 =====
function Connections({
  layout,
  positionsRef,
  hoveredId,
  selectedId,
}: {
  layout: LayoutItem[];
  positionsRef: React.MutableRefObject<Record<string, THREE.Vector3>>;
  hoveredId: string | null;
  selectedId: string | null;
}) {
  const lineRef = useRef<THREE.LineSegments>(null);
  const weakLineRef = useRef<THREE.LineSegments>(null);
  const geomRef = useRef<THREE.BufferGeometry>(null);
  const weakGeomRef = useRef<THREE.BufferGeometry>(null);

  // 分类边:同类(强连接,明显)+ 异类(弱连接,淡)
  const { strongEdges, weakEdges } = useMemo(() => {
    const strong: Array<[string, string]> = [];
    const weak: Array<[string, string]> = [];
    // 按 category 分组,同类内部全互连(聚拢感)
    const byCat: Record<string, typeof layout> = {};
    for (const item of layout) {
      const c = item.planet.category;
      (byCat[c] ||= []).push(item);
    }
    for (const items of Object.values(byCat)) {
      for (let i = 0; i < items.length; i++) {
        for (let j = i + 1; j < items.length; j++) {
          strong.push([items[i].planet.id, items[j].planet.id]);
        }
      }
    }
    // 异类之间:每组第一个连到另一组第一个(弱连接,表示跨领域)
    const cats = Object.values(byCat);
    if (cats.length >= 2) {
      for (let i = 0; i < cats.length; i++) {
        const a = cats[i][0].planet.id;
        const b = cats[(i + 1) % cats.length][0].planet.id;
        weak.push([a, b]);
      }
    }
    return { strongEdges: strong, weakEdges: weak };
  }, [layout]);

  useFrame(() => {
    // 更新强连接
    if (geomRef.current) {
      const posAttr = geomRef.current.attributes.position as THREE.BufferAttribute;
      const positions = posAttr.array as Float32Array;
      let idx = 0;
      for (const [a, b] of strongEdges) {
        const pa = positionsRef.current[a];
        const pb = positionsRef.current[b];
        if (!pa || !pb) continue;
        positions[idx++] = pa.x; positions[idx++] = pa.y; positions[idx++] = pa.z;
        positions[idx++] = pb.x; positions[idx++] = pb.y; positions[idx++] = pb.z;
      }
      posAttr.needsUpdate = true;
    }
    // 更新弱连接
    if (weakGeomRef.current) {
      const posAttr = weakGeomRef.current.attributes.position as THREE.BufferAttribute;
      const positions = posAttr.array as Float32Array;
      let idx = 0;
      for (const [a, b] of weakEdges) {
        const pa = positionsRef.current[a];
        const pb = positionsRef.current[b];
        if (!pa || !pb) continue;
        positions[idx++] = pa.x; positions[idx++] = pa.y; positions[idx++] = pa.z;
        positions[idx++] = pb.x; positions[idx++] = pb.y; positions[idx++] = pb.z;
      }
      posAttr.needsUpdate = true;
    }
  });

  return (
    <>
      {/* 强连接:同类,明显 */}
      <lineSegments ref={lineRef}>
        <bufferGeometry ref={geomRef}>
          <bufferAttribute
            attach="attributes-position"
            args={[new Float32Array(strongEdges.length * 6), 3]}
          />
        </bufferGeometry>
        <lineBasicMaterial
          color="#818cf8"
          transparent
          opacity={selectedId ? 0.15 : 0.35}
          blending={THREE.AdditiveBlending}
        />
      </lineSegments>
      {/* 弱连接:异类,淡 */}
      <lineSegments ref={weakLineRef}>
        <bufferGeometry ref={weakGeomRef}>
          <bufferAttribute
            attach="attributes-position"
            args={[new Float32Array(weakEdges.length * 6), 3]}
          />
        </bufferGeometry>
        <lineBasicMaterial
          color="#52525b"
          transparent
          opacity={selectedId ? 0.02 : 0.08}
          blending={THREE.AdditiveBlending}
        />
      </lineSegments>
    </>
  );
}

// ===== 单个星球:默认白色小光点,hover 高亮放大(不变色) =====
function PlanetMesh({
  planet,
  basePos,
  hoveredId,
  selectedId,
  onHover,
  onSelect,
  positionsRef,
}: {
  planet: Planet;
  basePos: [number, number, number];
  hoveredId: string | null;
  selectedId: string | null;
  onHover: (id: string | null) => void;
  onSelect: (id: string) => void;
  positionsRef: React.MutableRefObject<Record<string, THREE.Vector3>>;
}) {
  const groupRef = useRef<THREE.Group>(null);
  const sphereRef = useRef<THREE.Mesh>(null); // 白色球本体
  const haloRef = useRef<THREE.Mesh>(null); // 彩色光晕(身份标识)
  const hitRef = useRef<THREE.Mesh>(null); // 命中区(透明)

  const phase = useRef(basePos[0] * 1.7 + basePos[1] * 3.1);
  const formRef = useRef(0); // 0=光点 1=高亮球

  const isHovered = hoveredId === planet.id;
  const isSelected = selectedId === planet.id;
  const isOtherSelected = selectedId !== null && !isSelected;

  // 初始化共享位置
  if (!positionsRef.current[planet.id]) {
    positionsRef.current[planet.id] = new THREE.Vector3(...basePos);
  }

  useFrame((state, delta) => {
    if (!groupRef.current) return;
    const t = state.clock.elapsedTime;

    // 漂浮
    const driftX = Math.sin(t * 0.15 + phase.current) * 0.15;
    const driftY = Math.cos(t * 0.12 + phase.current) * 0.1;
    const driftZ = Math.sin(t * 0.1 + phase.current * 1.3) * 0.1;
    const focusBoost = (isHovered ? 1.5 : 0) + (isSelected ? 3 : 0);

    const tx = basePos[0] + driftX;
    const ty = basePos[1] + driftY;
    const tz = basePos[2] + driftZ + focusBoost;

    groupRef.current.position.x += (tx - groupRef.current.position.x) * 0.05;
    groupRef.current.position.y += (ty - groupRef.current.position.y) * 0.05;
    groupRef.current.position.z += (tz - groupRef.current.position.z) * 0.05;

    // 同步到共享位置(供连线层使用)
    positionsRef.current[planet.id].copy(groupRef.current.position);

    // 形变:hover/selected → 1,响应要快
    const targetForm = (isHovered || isSelected) ? 1 : 0;
    formRef.current += (targetForm - formRef.current) * 0.25;
    const f = formRef.current;

    // 白色球:默认小光点(0.08),hover 放大到高亮(0.25)
    if (sphereRef.current) {
      const scale = 0.08 + f * 0.18;
      sphereRef.current.scale.setScalar(scale);
      const mat = sphereRef.current.material as THREE.MeshBasicMaterial;
      // 始终白色,亮度通过 opacity 体现
      mat.opacity = isOtherSelected ? 0.25 : (0.85 + f * 0.15);
    }

    // 彩色光晕:仅 hover/selected 显现(身份标识,不变色本体)
    if (haloRef.current) {
      const haloScale = 0.08 + f * 0.5;
      haloRef.current.scale.setScalar(haloScale);
      const mat = haloRef.current.material as THREE.MeshBasicMaterial;
      mat.opacity = isOtherSelected ? 0 : (f * (isSelected ? 0.22 : 0.13));
    }

    // 命中区:始终略大于可见光晕,保证鼠标在可见球任何位置都能命中
    if (hitRef.current) {
      const hitScale = 0.15 + f * 0.7; // 默认 0.15 > 光点 0.08,hover 0.85 > 光晕 0.58
      hitRef.current.scale.setScalar(hitScale);
    }
  });

  return (
    <group ref={groupRef}>
      {/* 命中区:透明大球,半径随形变放大,始终包住可见球 */}
      <mesh
        ref={hitRef}
        onClick={(e) => {
          e.stopPropagation();
          onSelect(planet.id);
        }}
        onPointerOver={(e) => {
          e.stopPropagation();
          onHover(planet.id);
          document.body.style.cursor = 'pointer';
        }}
        onPointerOut={(e) => {
          e.stopPropagation();
          onHover(null);
          document.body.style.cursor = 'auto';
        }}
      >
        <sphereGeometry args={[1, 8, 8]} />
        <meshBasicMaterial transparent opacity={0} depthWrite={false} />
      </mesh>

      {/* 白色球本体(默认光点,hover 高亮,只负责视觉) */}
      <mesh ref={sphereRef}>
        <sphereGeometry args={[1, 16, 16]} />
        <meshBasicMaterial color="#ffffff" transparent opacity={0.85} blending={THREE.AdditiveBlending} />
      </mesh>

      {/* 彩色光晕 */}
      <mesh ref={haloRef}>
        <sphereGeometry args={[1, 16, 16]} />
        <meshBasicMaterial color={planet.color} transparent opacity={0} blending={THREE.AdditiveBlending} />
      </mesh>

      {/* 标签 */}
      {(isHovered || isSelected) && (
        <Html center distanceFactor={10} position={[0, 0.5, 0]} style={{ pointerEvents: 'none' }}>
          <div style={{
            color: '#e4e4e7',
            fontSize: '13px',
            fontWeight: 300,
            whiteSpace: 'nowrap',
            textShadow: '0 0 16px rgba(0,0,0,0.95)',
            letterSpacing: '0.15em',
          }}>
            {planet.name}
          </div>
        </Html>
      )}
    </group>
  );
}

// ===== 背景星云体积层 =====
function NebulaBackground() {
  return (
    <>
      <Stars radius={80} depth={50} count={2500} factor={3} saturation={0} fade speed={0.3} />
      <Sparkles count={80} scale={[30, 12, 20]} size={10} speed={0.15} color="#6366f1" opacity={0.25} />
      <Sparkles count={50} scale={[24, 10, 16]} size={14} speed={0.1} color="#a855f7" opacity={0.18} />
      <Sparkles count={120} scale={[20, 8, 12]} size={2} speed={0.4} color="#e0e7ff" opacity={0.5} />
    </>
  );
}

// ===== 星云主组件 =====
export default function Nebula({
  selectedId,
  onSelectPlanet,
}: {
  selectedId: string | null;
  onSelectPlanet: (id: string | null) => void;
}) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const positionsRef = useRef<Record<string, THREE.Vector3>>({});

  // 按 category 聚类布局:同类聚拢在一侧,组内紧凑排列
  const layout: LayoutItem[] = useMemo(() => {
    // 分两组
    const research = planets.filter((p) => p.category === 'research');
    const engineering = planets.filter((p) => p.category === 'engineering');

    const place = (items: Planet[], centerX: number, centerY: number): LayoutItem[] =>
      items.map((p, i) => {
        // 组内:小圆形聚拢
        const angle = (i / items.length) * Math.PI * 2;
        const r = 0.9;
        return {
          planet: p,
          basePos: [
            centerX + Math.cos(angle) * r,
            centerY + Math.sin(angle) * r * 0.6,
            Math.sin(angle) * 0.5,
          ] as [number, number, number],
        };
      });

    return [
      ...place(research, -2.2, 0.2),
      ...place(engineering, 2.2, -0.3),
    ];
  }, []);

  return (
    <Canvas
      camera={{ position: [0, 0.8, 8], fov: 50 }}
      style={{ width: '100%', height: '100%' }}
      dpr={[1, 2]}
      gl={{ antialias: true, alpha: true }}
      onCreated={(state) => {
        state.gl.setClearColor('#000000', 0);
      }}
    >
      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 3, 5]} intensity={0.5} color="#a5b4fc" />

      <NebulaBackground />

      <Connections
        layout={layout}
        positionsRef={positionsRef}
        hoveredId={hoveredId}
        selectedId={selectedId}
      />

      {layout.map(({ planet, basePos }) => (
        <PlanetMesh
          key={planet.id}
          planet={planet}
          basePos={basePos}
          hoveredId={hoveredId}
          selectedId={selectedId}
          onHover={setHoveredId}
          onSelect={onSelectPlanet}
          positionsRef={positionsRef}
        />
      ))}

      {/* 拖动旋转整个星云 */}
      <OrbitControls
        enableZoom={false}
        enablePan={false}
        autoRotate
        autoRotateSpeed={0.3}
        rotateSpeed={0.4}
        minPolarAngle={Math.PI / 3}
        maxPolarAngle={Math.PI / 1.8}
      />

      {/* 点击空白取消 */}
      <mesh onClick={() => onSelectPlanet(null)} position={[0, 0, -3]} visible={false}>
        <planeGeometry args={[100, 100]} />
        <meshBasicMaterial transparent opacity={0} />
      </mesh>
    </Canvas>
  );
}
