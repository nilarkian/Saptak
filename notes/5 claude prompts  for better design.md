---
project:
  - "[[AI Agent Manager + CLAUDE]]"
---

### **01  The Visual Hierarchy Surgeon**

```js
I'm going to share a design with you.Your job is to act as a visual hierarchy surgeon, not a compliment machine. 

 Do this in order:                                                                  
 1.  Tell me where the eye lands first, second, and third — based purely             on size, contrast, color weight, and position. 
 2.  Tell me where the eye SHOULD land first, second, and third — based              on the business or communication goal. 
 3.  Identify every element that is competing for attention it hasn't earned.        For each problem, give me one specific fix: exact font size change, 
 contrast adjustment, spacing tweak, or removal.                                    
 Rules:                                                                             
 - No vague feedback like 'improve the hierarchy.' Name the element, name the fix. 
 - If something needs to be removed entirely, say so.                              
 - Rank your fixes by impact. What one change would do the most work?              
```

 

### **02  The Typography Interrogation**

 ```js
Audit the typography in this design like a senior type director.  Go through each of these checkpoints and give me a verdict + fix for each:   
 
 1. PAIRING 
     - Do the fonts create tension or harmony? Is that the right call for this context? 
     - Are the fonts doing distinct jobs or are they stepping on each other? 
 2. SCALE 
     - Is there enough size contrast between heading levels? 
     - Does the smallest text stay readable at actual viewing distance? 
 3. SPACING 
     - Is line-height set for readability or left at default? 
     - Is letter-spacing on headlines tightened? On all-caps labels, loosened? 
     - Are paragraph widths within the 60-75 character ideal? 
 4. WEIGHT 
     - Is font weight doing contrast work, or just decorative? 
     - Are there bold elements replaceable by size contrast instead? 
 5. HIERARCHY SIGNAL 
     - Can someone tell the difference between primary, secondary, and tertiary  text at a glance? 
   
 ```
 

### **03  The Whitespace Pressure Test**

```js
Pressure-test the whitespace and spacing in this design. 

   
 MACRO SPACING (sections, containers) 
 - Are section gaps large enough to signal a new zone, or do sections bleed together? 
 - Is there a consistent spatial rhythm (e.g., 8pt grid) or does spacing feel ad hoc? 
   
 MICRO SPACING (components, text, icons) 
 - Inside cards and components, is padding equal on all sides or does it look squeezed? 
 - Do icons have enough clearance from adjacent text? 
 - Are button labels getting enough horizontal padding? 
   
 BREATHING ROOM 
 - Which elements need more isolation to feel important? 
 - Where is whitespace being filled out of fear instead of intention? 
   
 PERCEIVED VALUE 
 - Would increasing padding in any area make the design feel more premium? 
 - Are there dense areas that could be split across two sections instead of one? 
   
 Give me specific pixel recommendations. If the design uses a component library, 
 tell me which spacing tokens or utility classes to change. 
```
### **04  The Color & Contrast Stress Test**

 ```js
 Run a full color and contrast audit on this design. 

   
 PALETTE LOGIC 
 - How many colors are actively in use? List them. 
 - Is there a clear dominant, secondary, and accent structure, or are colors 
   roughly equal weight? 
 - Do any colors feel like they were added 'just because'? 
   
 EMOTIONAL SIGNAL 
 - What does this palette communicate emotionally? 
   (e.g., clinical, warm, energetic, trustworthy, playful) 
 - Is that the right signal for the product and audience? 
 - Is there tension between what the colors say and what the product promises? 
   
 ACCESSIBILITY 
 - Flag any text/background combinations below WCAG AA 
   (4.5:1 for body, 3:1 for large text). 
 - Are interactive elements distinguishable from non-interactive ones? 
   
 SOPHISTICATION 
 - Is the accent color being overused? 
 - Are there neutrals in the palette? Do they feel considered or left at defaults? 
 - Would swapping any color for a muted version increase perceived quality? 
   
 Give me hex values for any suggested replacements. 
 ```  

### **05  The 'Why Does This Look Cheap?' Diagnosis**
```js
 Forget the positives for now. I need a brutally honest diagnosis. 
 THE DIAGNOSIS 
 - Name the 3 specific reasons this looks underdeveloped, low-budget, or unfinished. 
 - For each reason, tell me: what visual signal is creating that impression? 
   
 THE ROOT CAUSE 
 - Is the core problem typography, spacing, color, layout, component quality, 
   or consistency? 
 - If you had to fix only ONE thing that would immediately shift the perceived 
   quality, what is it? 
   
 THE 10X TREATMENT 
 - Give me the 3 changes that would make this design look like it cost 10x more. 
 - Order them by impact. 
 - For each: what specifically changes, and why does that change signal premium 
   quality to a viewer? 
   
 WHAT TO KEEP 
 - Name one thing in this design that is already working and should not be changed. 
   
 Be direct. I want a design doctor, not a design cheerleader. 
```
**Pro tip:** Prompt 5 gives you the headline problem fast. Prompts 1–4 fix each layer systematically. Use them together on the same design file for a complete audit.
