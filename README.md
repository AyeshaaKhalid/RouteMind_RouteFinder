# RouteMind: Intelligent Route Finder using Fuzzy Logic and A*

## Group Members
- Mishkat Fatima – 221336  
- Ayesha Khalid – 221408  
- Aamna Ibrahim Qureshi – 221438  

## Project Summary

RouteMind is an AI-powered route optimization system that calculates the best path between two points using A* pathfinding and fuzzy logic. Unlike traditional navigation algorithms, RouteMind considers real-world conditions such as traffic, weather, road surface, time of day, and road type to generate dynamic route costs and smarter navigation suggestions.

## Setup & Run Instructions

1. Clone the repository:
```bash
git clone https://github.com/AyeshaahKhalid/RouteMind_RouteFinder.git
cd RouteMind_RouteFinder/src
```  

## **AI Techniques Used and Justification**

**Fuzzy Logic:**
 - Used to model subjective and imprecise real-world conditions such as traffic, weather, road quality, 
   and time of day.
 - Converts these conditions into fuzzy sets (e.g., low, average, high) using membership functions.
 - Fuzzy rules (IF-THEN statements) define how these inputs affect route cost.
 - Output is a dynamic cost value that mimics human reasoning.

**A* Pathfinding Algorithm:**
 - Finds the most efficient path between two points using heuristic search.
 - Considers both actual travel cost and estimated cost to reach the destination (via Euclidean distance).
 - Integrated with fuzzy output to adjust edge weights dynamically.

**Justification:**
 - Real-world navigation is uncertain — fuzzy logic handles that uncertainty intelligently.
 - A* ensures optimal route selection while fuzzy logic enhances decision-making under real-world 
   complexity.
 - The combination provides a smart, adaptive system unlike traditional rigid algorithms.
