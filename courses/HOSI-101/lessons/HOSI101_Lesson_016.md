# HOSI-101 — Lesson 16: Neural Networks

**Status:** Source-verified draft — human academic/safety/accessibility review pending  
**Lesson ID:** HOSI-101-016  
**Module:** 02 — Neuroscience Foundations  
**Difficulty:** Foundational  
**Estimated time:** 65–80 min  
**Evidence level:** A/B for connectivity concepts; B/C for some network-model interpretations  
**Domain tags:** neural networks; structural connectivity; functional connectivity; effective connectivity; graph theory  
**Study-path tags:** Neuroscience Foundations; Research Literacy; all condition study paths  
**Prerequisites:** Lessons 11–15  
**Revision date:** 2026-09-16  
**Review state:** AI-assisted source verification complete; independent human review pending

## 1. Original visual / cover

Visual brief: the same six brain regions shown three ways: anatomical fiber pathways, correlated activity, and directional influence model. Labels read structural connectivity, functional connectivity, and effective connectivity.

Accessible alt text: three network diagrams illustrating that physical connections, statistical co-activity, and modeled directional influence are distinct forms of connectivity evidence.

## 2. Why this matters

“Connectivity changed” sounds impressive and tells you almost nothing until you ask **what kind of connectivity, measured how, between which nodes, during what state, and with what interpretation?**

Network neuroscience provides powerful tools for studying distributed brain organization, but different connectivity measures answer different questions. [F21][F22]

## 3. Learning objectives

- distinguish structural, functional, and effective connectivity;
- explain nodes, edges, hubs, modules, and network topology;
- describe why correlation between regions does not prove direct anatomical connection or causal influence;
- explain structure-function coupling and its variability;
- identify why group-level network findings are not automatically individual biomarkers.

## 4. Vocabulary

node; edge; network; graph; structural connectivity; functional connectivity; effective connectivity; hub; module; centrality; coupling; connectome; correlation; directionality

## 5. Normal human-system baseline

Brain activity is coordinated across multiple scales. Anatomical pathways constrain communication, but functional relationships change with task, sleep/wake state, learning, development, and measurement method. The same structural connection can participate differently across contexts.

## 6. Core science

[A/B] **Structural connectivity** describes physical anatomical pathways, commonly estimated in humans with diffusion MRI or traced directly in nonhuman/other preparations.

[A/B] **Functional connectivity** usually refers to statistical dependence or correlation among signals. It does not require a direct anatomical connection and does not by itself establish causal direction.

[B] **Effective connectivity** attempts to model directed influence among components using assumptions about system dynamics. Its interpretation depends strongly on the chosen model and data.

[B] Structure-function coupling varies across regions, people, tasks, and states rather than following one fixed relationship. [F22]

[B] EEG connectivity methods differ in sensitivity to volume conduction, reference choices, frequency bands, preprocessing, and estimator assumptions. [F21]

## 7. Network concepts

### Nodes and edges
Nodes may represent neurons, regions, parcels, nuclei, or sensors. Edges represent relationships defined by the measurement method.

### Hubs
Nodes with unusually high centrality or integrative roles in a defined network. A “hub” depends on how the network is constructed.

### Modules/communities
Groups of nodes more strongly connected with each other than with the rest of the network under a chosen method.

### Dynamic networks
Functional relationships change over time. A resting-state network is not a permanent wiring diagram.

### Structure-function coupling
Anatomy constrains function without determining it completely. The relationship itself differs across the brain. [F22]

## 8. Evidence map

- **A/B —** distinct structural and functional connectivity constructs are well established.
- **B —** effective-connectivity estimates are useful but model-dependent.
- **B —** structure-function coupling is heterogeneous and context dependent. [F22]
- **B —** technical choices materially affect connectivity estimates. [F21]

## 9. What is known

Distributed brain function depends on communication among specialized components. Network approaches can reveal organizational patterns that single-region analyses miss.

## 10. What remains uncertain

Different parcellations, preprocessing pipelines, statistical thresholds, and network metrics can produce different results. The field continues debating which network features are most stable, causal, clinically useful, and individually predictive.

## 11. Condition-specific applications

Connectivity differences have been reported across many psychiatric and neurological conditions. Overlap across diagnoses is common, and most findings are not specific enough to diagnose one person. HOSI should report effect size, replication, population, method, and classification performance before using biomarker language.

## 12. Combination/comorbidity lens

When conditions co-occur, observed network differences may reflect shared symptoms, medication, sleep, development, injury, environment, or multiple mechanisms. A network signature does not automatically identify one causal diagnosis.

## 13. Lived-experience perspective

A person may experience attention, emotion, or movement as “disconnected.” That description can be meaningful but is not equivalent to a measured connectivity abnormality.

## 14. Practical skill / exercise

For each statement, identify the evidence type and what cannot be concluded:
1. “Diffusion MRI suggests reduced integrity in tract X.”
2. “Regions A and B show correlated resting-state signals.”
3. “A model estimates stronger directed influence from A to B.”
4. “A network classifier separates two study groups at 72% accuracy.”

## 15. Safety / scope

This lesson does not interpret personal MRI, EEG, qEEG, consumer-neurotechnology, or brain-network reports. Connectivity findings require method-specific professional interpretation and usually do not function as standalone diagnoses.

## 16. Cornell Notes

Cue terms: structural, functional, effective, node, edge, hub, coupling.  
Summary: “What does each type of connectivity actually allow us to claim?”

## 17. Reflection

Why is the word “connected” potentially misleading when used without a measurement definition?

## 18. Discussion prompt

If two regions have strong functional connectivity but no direct anatomical pathway, is that surprising? Explain network routes and common inputs.

## 19. Knowledge check / quiz

1. Define structural connectivity.
2. Define functional connectivity.
3. What does effective connectivity attempt to estimate?
4. Why can functional connectivity exist without a direct structural edge?
5. What is structure-function coupling?
6. Why is a network hub method-dependent?

## 20. Homework

Choose one published connectivity figure. Identify nodes, edge definition, measurement method, population, state/task, and three conclusions the figure does **not** justify.

## 21. Scholar challenge

Find two papers studying the same network with different modalities (for example fMRI and EEG). Compare what each modality can and cannot infer.

## 22. Instructor answer key / rubric

Strong work keeps structural, functional, and effective connectivity separate; identifies methodological assumptions; and resists causal or diagnostic inflation. Students should not be rewarded for producing a fashionable graph without defining its edges.

## 23. References

- [F21] Connectivity Analysis in EEG Data: A Tutorial Review of the State of the Art and Emerging Trends. 2023. https://pubmed.ncbi.nlm.nih.gov/36978763/
- [F22] Fotiadis P, et al. Structure-function coupling in macroscale human brain networks. 2024. DOI: 10.1038/s41583-024-00846-6. https://pubmed.ncbi.nlm.nih.gov/39103609/
- [F13] Du J, et al. Organization of the human cerebral cortex estimated within individuals. 2024. DOI: 10.1152/jn.00308.2023. https://pubmed.ncbi.nlm.nih.gov/38489238/
- [F19] Hansen JY, et al. Integrating brainstem and cortical functional architectures. 2024. https://pubmed.ncbi.nlm.nih.gov/39414973/

## 24. Further reading

Read a connectivity-methods paper and list every analytical choice made between raw data and the final network figure.

## 25. Research update log

- 2026-09-16 — Canonical manuscript drafted; structural/functional/effective distinctions and structure-function heterogeneity incorporated.
- Next gate — network-neuroscience methods, statistics, accessibility, assessment, and citation review.

## 26. What would change our mind?

More robust causal methods, standardized reproducible pipelines, or validated individual biomarkers that materially change current interpretation limits should trigger revision.