# Agentic RAG Assignment

This repository contains the implementation of an Agentic RAG (Retrieval-Augmented Generation) system using Autogen, designed to process complex queries through multi-agent collaboration. The system intelligently retrieves relevant information from various knowledge sources and generates accurate, contextual responses enhanced with retrieved knowledge.

## System Architecture
![Agentic RAG Architecture]([https://i.imgur.com/placeholder.png](https://github.com/codeloki15/Agentic_RAG/blob/main/agentic_rag.png))

The above diagram illustrates our multi-agent architecture:
1. User queries are sent to Agent1 (Assistant agent) which identifies question intent and entities
2. Agent2 (Assistant agent) refines the question intent and entities
3. Agent3 (User-proxy agent) performs vector extraction using the query, intent, and entities to retrieve the top K chunks
4. Agent4 (Assistant agent) combines the original question with the retrieved chunks to generate a comprehensive response

## Agentic RAG Assignment – Two-Week Plan

**Start Date:** [Insert Start Date]  
**Final Submission Date:** [Insert Date, Two Weeks Later]

## Objective

Create a group of agents using Autogen that implements an advanced RAG system capable of answering complex queries by retrieving relevant information from multiple knowledge sources. Agents should collaborate to understand queries, retrieve pertinent information, reason over the retrieved context, and generate comprehensive responses.

## Week 1: Research, Planning, and Initial Development

### Day 1-2: Understanding RAG & Multi-Agent Collaboration
- Study Autogen's documentation and multi-agent framework
- Research RAG systems and their implementations
- Explore vector databases (e.g., Chroma, Pinecone, FAISS)
- Understand embedding models and similarity search

### Day 3-4: System Architecture & Knowledge Base Setup
- Define agent roles and communication workflows
- Set up vector database for document storage
- Implement document chunking and embedding strategies
- Design query processing and retrieval mechanisms

### Day 5-7: Initial Implementation & Basic Functionality
- Implement query parsing and understanding
- Create retrieval mechanism for relevant documents
- Develop basic response generation using retrieved context
- Ensure system correctly processes simple queries

### End of Week 1 Deliverables:
- ✅ Basic agent-based RAG system setup
- ✅ Working document retrieval and basic response generation
- ✅ Documented architecture plan

## Week 2: Feature Expansion, Testing, and Finalization

### Day 8-9: Enhancing Functionality & Multi-Source Support
- Improve query understanding with more sophisticated parsing
- Implement cross-document reasoning capabilities
- Add support for multiple knowledge sources (docs, APIs, etc.)
- Enhance retrieval quality with reranking and filtering

### Day 10-11: Advanced Features & Performance Optimization
- Implement self-reflection and response refinement
- Add citation and attribution to source documents
- Optimize retrieval speed and accuracy
- Implement conversational memory for follow-up questions

### Day 12: Testing & Debugging
- Test with diverse query types and domains
- Benchmark performance against baseline RAG systems
- Fix bottlenecks and optimize agent communication
- Evaluate answer quality and factual accuracy

### Day 13: Documentation & Demo Preparation
- Write detailed README with setup instructions
- Document key challenges and solutions
- Prepare demonstration queries showcasing system capabilities

### Day 14: Final Submission
- Submit code, documentation, and test results
- Ensure everything is properly packaged for review
- Demo the complete functionality on a live call with evaluation team

## Evaluation Criteria (100 Points)

### 1. Functionality (40 Points)
- 0 Points: Solution doesn't work
- 10 Points: Solution works but is highly unstable
- 30 Points: Solution works but only on specific knowledge domains
- 40 Points: Solution works across multiple knowledge domains with high accuracy

### 2. Code Quality & Documentation (20 Points)
- Is the code well-structured, modular, and easy to understand? (10 Points)
- Is there proper documentation, setup guide, and architecture explanation? (10 Points)

### 3. Retrieval Quality (15 Points)
- Does the system retrieve relevant information accurately? (5 Points)
- Are retrieval results properly ranked and filtered? (5 Points)
- Can the system handle ambiguous or complex queries? (5 Points)

### 4. Innovation & Complexity (15 Points)
- Are there advanced features like self-critique or multi-hop reasoning? (5 Points)
- Is the solution optimized for both speed and accuracy? (5 Points)
- Is there efficient use of multi-agent collaboration? (5 Points)

### 5. Production Readiness (10 Points)
- 0 Points: The solution is not usable in real-world scenarios
- 5 Points: The solution is functional but lacks refinement
- 10 Points: The solution is well-optimized and production-ready

## Total Score Calculation
- 0 Points – Non-functional solution
- 0.3x (30%) – Works only on specific knowledge domains
- 0.8x (80%) – Works on multiple domains with good accuracy
- 1x (100%) – Works across domains, has good code, and is production-ready

## Submission Requirements
- GitHub Repository with code, documentation, and test results
- Application Demo (5-10 min) explaining functionality and design decisions
- Performance metrics comparing your system to baseline approaches

## Submission Format
- Codebase with clear structure and dependency management
- ReadMe file with comprehensive setup and usage instructions
- Test suite with evaluation metrics and example queries
- Demo on live call showcasing key capabilities

*All points awarded shall be at the sole discretion of the evaluation team, and their decision shall be final and binding.*
