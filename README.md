# 🏎️ Formula 1 Strategy Evolution

**Author:** Aleksandar Zekovic, 2025

---

## 🎯 What Is This?

Evolving Formula 1 race strategies using Genetic Programming. Instead of coding strategies by hand, evolution discovers them through simulation.

The system evolves decision trees that make strategic calls:
- **When to pit stop?**
- **Which tyres?** (Soft/Medium/Hard/Intermediate/Wet)
- **Push hard or save tyres?**

Strategies react to:
- Tyre wear and age
- Safety car deployments
- Rain probability and track wetness
- Race position and gaps to rivals
- Current lap number

**Run it:**
```bash
python3 main.py
```

---

## 📊 Test Results

### Latest Run (100 Generations, Population 50, Seed 42)

**Evolution Progress:**
```
Gen   0 | 🏆 Best: 4588.6s | 📊 Top 10 avg: 4679.7s
Gen  10 | 🏆 Best: 4565.0s | 📊 Top 10 avg: 4573.9s
Gen  20 | 🏆 Best: 4565.0s | 📊 Top 10 avg: 4571.2s
Gen  40 | 🏆 Best: 4563.4s | 📊 Top 10 avg: 4572.9s
Gen  60 | 🏆 Best: 4563.4s | 📊 Top 10 avg: 4569.3s
Gen  80 | 🏆 Best: 4561.9s | 📊 Top 10 avg: 4570.7s
Gen 100 | 🏆 Best: 4561.9s | 📊 Top 10 avg: 4572.7s
```

**Performance:**
- Initial fitness: 4588.6 seconds
- Final fitness: 4561.9 seconds
- Improvement: 26.7 seconds (0.58%)
- Convergence: ~40 generations

### Evolved Strategy Highlights

Key insights discovered by evolution:

1. **Position-aware decisions:**
   - If position > 15 → Stay out on Hard tyres, push hard

2. **Safety car exploitation:**
   - Under safety car + rain → Pit for Wet tyres

3. **Tyre management:**
   - Soft tyres over 12 laps old → Consider pit stop
   - Hard tyres over 25 laps old → Definitely pit

4. **Weather adaptation:**
   - Track wetness > 0.6 → Switch to wet tyres
   - Track wetness > 0.3 → Conservative pace

### Scenario Testing

| Situation | Decision | Why? |
|-----------|----------|------|
| Lap 10, P3, Soft (5 laps) | Stay out, push | Tyres fresh |
| Lap 25, P8, Safety car | Stay out | Mediums OK |
| Lap 45, P5, Hard (30 laps) | **PIT**, conservative | Old + rain |
| Lap 5, P15, Soft (3 laps) | Stay out, push | Attack |
| Lap 20, P6, Wet track (0.6) | Stay out, careful | Wrong tyres |

---

## 🧬 How It Works

### 1. Representation: Decision Trees

Strategies are encoded as trees:

```
? tyre_age > 25
  Y ? gap_to_rival < 1.0
    Y → PIT: True, TYRES: Medium
    N → PIT: False, TYRES: Soft
  N → PIT: False, TYRES: Hard
```

Each node:
- **Condition node:** Evaluates race state, branches left/right
- **Action node:** Returns decision (pit/tyres/pace)

### 2. Fitness Evaluation

Strategies simulate 3 races, average total time:

```python
base_time = 90.0 seconds
+ tyre_degradation (Soft degrades fastest)
+ compound_speed (Soft fastest, Hard slowest)
+ safety_car_time (if deployed)
+ wrong_tyres_penalty (dry on wet = +5s)
- aggressive_bonus (if pushing hard)
= lap_time
```

**Penalties:**
- No pit stops: +100s (illegal)
- Too many pits (>3): +50s each
- Pit stop: 25s (save 10s under safety car)

### 3. Evolution Process

```
1. INITIALIZE: Create 50 random trees
    ↓
2. EVALUATE: Simulate races, calculate fitness
    ↓
3. SELECT: Tournament selection (top performers)
    ↓
4. CROSSOVER: Swap subtrees between parents
    ↓
5. MUTATE: Random changes to conditions/actions
    ↓
6. REPEAT: For 100 generations
```

### 4. Genetic Operators

**Tournament Selection:**
- Pick 3 random strategies
- Select best (lowest race time)

**Subtree Crossover:**
```
Parent 1:       Parent 2:
   [A]             [X]
   / \             / \
  B   C           Y   Z

Child 1:        Child 2:
   [A]             [X]
   / \             / \
  Y   C           B   Z
```

**Mutation:**
- Change condition: `tyre_age > 15` → `tyre_age > 20`
- Change action: `PIT: True` → `PIT: False`
- Change compound: `Soft` → `Medium`

---

## 🏁 F1 Racing Context

### Tyre System (FIA Official)

| Compound | Color | Speed | Durability | Use Case |
|----------|-------|-------|------------|----------|
| **Soft** | 🔴 Red | ★★★★★ | ★★☆☆☆ | Qualifying, short stints |
| **Medium** | 🟡 Yellow | ★★★★☆ | ★★★★☆ | Balanced race strategy |
| **Hard** | ⚪ White | ★★★☆☆ | ★★★★★ | Long stints, high deg tracks |
| **Inter** | 🟢 Green | ★★★☆☆ | ★★★☆☆ | Light rain, drying track |
| **Wet** | 🔵 Blue | ★★☆☆☆ | ★★★★☆ | Heavy rain |

### Strategy Trade-offs

**Undercut Strategy:**
- Pit early on fresh tyres
- Gain time while rivals on old tyres
- Risk: Lose track position if overcut

**Overcut Strategy:**
- Stay out longer than rivals
- Hope they get stuck in traffic
- Risk: Tyre degradation

**Safety Car Gamble:**
- Pit during safety car (cheap stop)
- Gain advantage if timing right
- Risk: Stuck if SC ends quickly

Real F1 teams use:
- Real-time telemetry (100+ sensors)
- Weather forecasting
- Traffic and rival monitoring
- Game theory models

Our evolved strategies discover similar patterns autonomously!

---

## 🔬 Technical Details

### Key Algorithms

**Tyre Degradation Model:**
```python
degradation_per_lap = {
    Soft: 0.15s,      # High wear
    Medium: 0.08s,    # Moderate
    Hard: 0.05s,      # Low wear
    Intermediate: 0.10s,
    Wet: 0.12s
}
time_loss = tyre_age * degradation_rate
```

**Compound Speed (dry track):**
```python
Soft:    -1.0s  (fastest)
Medium:   0.0s  (baseline)
Hard:    +0.8s  (slowest)
Inter:   +2.0s  (wrong compound)
Wet:     +4.0s  (very wrong)
```

**Weather Penalties:**
```python
if track_wetness > 0.5 and dry_tyres:
    penalty = +5.0s per lap
if track_wetness < 0.2 and wet_tyres:
    penalty = +3.0s per lap
```

### Convergence Analysis

Evolution pattern:
- **Gen 0-20:** Rapid improvement (discover pit stops needed)
- **Gen 20-50:** Refinement (optimize pit timing)
- **Gen 50-100:** Fine-tuning (edge cases, weather handling)

Indicates:
- ✅ Fitness landscape is smooth enough
- ✅ Population diversity maintained (elitism works)
- ✅ Mutation rate balanced (not too disruptive)
