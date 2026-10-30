# Bit Pattern Generator using Genetic Algorithm

**Course:** BSD3513 Introduction to Artificial Intelligence  
**Topic:** Chapter 2: Search Algorithms (Lab Report 2 - Question 2)  

## Project Overview
This project is a Python web application built with **Streamlit**. It uses a **Genetic Algorithm (GA)** to generate an 80-bit binary pattern (a string of `0`s and `1`s) that reaches a specific target of **50 ones**. 

---

## Live Demo
- **Try to run Streamlit Web App here:** https://ai-labreport2-genetic-algorithm.streamlit.app/
---

## Problem Conditions 
The Genetic Algorithm is built to follow five fixed rules:
1. **Population Size:** 300 individuals per generation
2. **Target Number of Ones:** The fitness formula reaches its highest score when there are exactly **50 ones**
3. **Individual Length (Chromosome):** 80 bits (zeros and ones)
4. **Maximum Fitness Value:** 80 (achieved when the number of ones equals 50)
5. **Number of Generations:** 50 generations

---

## How the Algorithm Works
1. **Initialization:** Creates 300 random bit patterns, each with a length of 80 bits (`0` or `1`).
2. **Fitness Calculation:** Checks how good each pattern is using the formula:
   $$\text{Fitness} = 80 - |\text{Number of Ones} - 50|$$
   If a pattern has 50 ones, the difference is 0, giving the maximum fitness score of **80**.
3. **Tournament Selection:** Picks random small groups (default size $k = 3$) and chooses the fittest individuals to become parents.
4. **Single-Point Crossover:** Combines two parents at a random cut point to create two new children (default rate = `0.9`).
5. **Bit-Flip Mutation:** Randomly flips a small number of bits (`0` to `1` or `1` to `0`) to keep variety in the population (default rate = `0.0125`).
6. **Evolution:** Repeats this process for 50 generations until the optimal bit pattern is found.

---

## Features of the Web App
- **Interactive Sidebar:** Adjust the **Crossover Rate**, **Mutation Rate**, **Tournament Size ($k$)**, and **Random Seed**, or reset to default values with one click.
- **Live Progress Chart:** Watch the best and average fitness scores improve in real time across all 50 generations.
- **Final Results Summary:** Displays the best fitness score, total count of `1`s and `0`s, the exact generation where the optimum was first found, and the complete 80-bit string.
- **Convergence Graph & CSV Export:** View a clean Matplotlib convergence chart and download the generation-by-generation fitness data as a `.csv` file.

---
## Example Output
<img width="1093" height="828" alt="image" src="https://github.com/user-attachments/assets/74f9adc2-1a52-47e0-8597-68692e96dd5d" />


---
## How to Run This Project Locally

### 1. Clone the repository
```bash
git clone <your-github-repo-url>
cd <your-repo-folder>
