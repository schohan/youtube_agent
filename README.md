# Youtube Agent with Topic Ontology
> NOTE: This code is for proof of concept and is not meant for use in production environment.


## Overview

This AI agent is a TL;DR (or Too Long;Did't Watch ) helper for Youtube videos that can aid learning about a topic without having to find, filter, and watch unnecessary videos.

Even though you can search Youtube to find relevant videos, it is still difficult to know which videos are the most relevant by just looking at the thumbnail and titles of the videos. 

This agent helps to not only find the most relevant videos for a given topic but also summarizes the transcripts of each video for quick preview. It helps to save time as one can filter out a handful of videos to watch instead of watching all of them or spending time on the ones that are not relevant.

Applications built on top of this agent can help pinpoint the videos relevant to your needs. 

### How it works

1. User inputs a top level category. E.g. "Machine Learning"

2. Agent creates a curriculum (ontology), a mind-map of sorts, with relevant sub-categories and topics

Example ontology:
```
{
  "title": "Machine Learning",
  "description": "A comprehensive mind map for understanding the field of machine learning, covering its main branches, sub-branches, and key concepts.",
  "topics": [
    {
      "title": "Supervised Learning",
      "children": [
        {
          "title": "Regression",
          "children": [
            {
              "title": "Linear Regression",
              "children": null
            },
            {
              "title": "Polynomial Regression",
              "children": null
            },
            {
              "title": "Ridge Regression",
              "children": null
            },
            {
              "title": "Lasso Regression",
              "children": null
            }
          ]
        },
        {
          "title": "Classification",
          "children": [
            {
              "title": "Logistic Regression",
              "children": null
            },
            {
              "title": "Support Vector Machines",
              "children": null
            },
            {
              "title": "Decision Trees",
              "children": null
            },
            {
              "title": "Random Forest",
              "children": null
            },
            {
              "title": "K-Nearest Neighbors",
              "children": null
            },
            {
              "title": "Naive Bayes",
              "children": null
            }
          ]
        },
        {
          "title": "Evaluation Metrics",
          "children": [
            {
              "title": "Accuracy",
              "children": null
            },
            {
              "title": "Precision",
              "children": null
            },
            {
              "title": "Recall",
              "children": null
            },
            {
              "title": "F1 Score",
              "children": null
            },
            {
              "title": "ROC Curve",
              "children": null
            },
            {
              "title": "Confusion Matrix",
              "children": null
            }
          ]
        }
      ]
    },
    {
      "title": "Unsupervised Learning",
      "children": [
        {
          "title": "Clustering",
          "children": [
            {
              "title": "K-Means",
              "children": null
            },
            {
              "title": "Hierarchical Clustering",
              "children": null
            },
            {
              "title": "DBSCAN",
              "children": null
            }
          ]
        },
        {
          "title": "Dimensionality Reduction",
          "children": [
            {
              "title": "Principal Component Analysis (PCA)",
              "children": null
            },
            {
              "title": "t-Distributed Stochastic Neighbor Embedding (t-SNE)",
              "children": null
            },
            {
              "title": "Linear Discriminant Analysis (LDA)",
              "children": null
            }
          ]
        }
      ]
    },
    {
      "title": "Reinforcement Learning",
      "children": [
        {
          "title": "Markov Decision Processes",
          "children": null
        },
        {
          "title": "Q-Learning",
          "children": null
        },
        {
          "title": "Deep Q-Networks",
          "children": null
        },
        {
          "title": "Policy Gradient Methods",
          "children": null
        }
      ]
    },
    {
      "title": "Deep Learning",
      "children": [
        {
          "title": "Neural Networks",
          "children": [
            {
              "title": "Feedforward Neural Networks",
              "children": null
            },
            {
              "title": "Convolutional Neural Networks (CNN)",
              "children": null
            },
            {
              "title": "Recurrent Neural Networks (RNN)",
              "children": null
            }
          ]
        },
        {
          "title": "Training Techniques",
          "children": [
            {
              "title": "Backpropagation",
              "children": null
            },
            {
              "title": "Gradient Descent",
              "children": null
            },
            {
              "title": "Stochastic Gradient Descent",
              "children": null
            }
          ]
        },
        {
          "title": "Frameworks",
          "children": [
            {
              "title": "TensorFlow",
              "children": null
            },
            {
              "title": "PyTorch",
              "children": null
            },
            {
              "title": "Keras",
              "children": null
            }
          ]
        }
      ]
    },
    {
      "title": "Model Selection and Optimization",
      "children": [
        {
          "title": "Cross-Validation",
          "children": null
        },
        {
          "title": "Grid Search",
          "children": null
        },
        {
          "title": "Random Search",
          "children": null
        },
        {
          "title": "Bayesian Optimization",
          "children": null
        }
      ]
    },
    {
      "title": "Data Preprocessing",
      "children": [
        {
          "title": "Normalization",
          "children": null
        },
        {
          "title": "Standardization",
          "children": null
        },
        {
          "title": "Handling Missing Values",
          "children": null
        },
        {
          "title": "Feature Engineering",
          "children": null
        }
      ]
    },
    {
      "title": "Ethics and Fairness",
      "children": [
        {
          "title": "Bias in Algorithms",
          "children": null
        },
        {
          "title": "Transparency",
          "children": null
        },
        {
          "title": "Accountability",
          "children": null
        },
        {
          "title": "Privacy Concerns",
          "children": null
        }
      ]
    }
  ]
}
```

3. A human reviews the ontology and makes changes if needed (optional).

4. Agent then uses the topics in curriculum (leaf nodes + sub-topics) as query to search for youtube videos (tutorials). Videos are filtered based on minimum view and comment counts as well as their age (configurable).

5. Agent extracts video metadata and summarizes the transcripts of each video for quick preview. It helps to save time as one can watch the most relevant videos without watching all of them.

Example of a video metadata:
```
[
  {
    "video_id": "ErnWZxJovaM",
    "title": "MIT Introduction to Deep Learning | 6.S191",
    "description": "MIT Introduction to Deep Learning 6.S191: Lecture 1\n*New 2024 Edition*\nFoundations of Deep Learning\nLecturer: Alexander Amini\n\nFor all lectures, slides, and lab materials: http://introtodeeplearning.com/\n\nLecture Outline\n0:00\u200b - Introduction\n7:25\u200b - Course information\n13:37\u200b - Why deep learning?\n17:20\u200b - The perceptron\n24:30\u200b - Perceptron example\n31;16\u200b - From perceptrons to neural networks\n37:51\u200b - Applying neural networks \n41:12\u200b - Loss functions\n44:22\u200b - Training and gradient descent\n49:52\u200b - Backpropagation\n54:57\u200b - Setting the learning rate\n58:54\u200b - Batched gradient descent\n1:02:28\u200b - Regularization: dropout and early stopping\n1:08:47 - Summary\n\nSubscribe to stay up to date with new deep learning lectures at MIT, or follow us on @MITDeepLearning on Twitter and Instagram to stay fully-connected!!",
    "published_at": "2024-04-29T14:00:07+00:00",
    "view_count": 833893,
    "comment_count": 384,
    "like_count": 18061,
    "favorite_count": 0,
    "channel_title": "Alexander Amini",
    "transcript": "[Music] good afternoon everyone and welcome to MIT sus1 191 my name is Alexander amini and I'll be one of your instructors for the course this year along with Ava and together we're really excited to welcome you to this really incredible course this is a very fast-paced and very uh intense one week that we're about to go through together right so we're going to cover the foundations of a also very fast-paced moving field and a field that has been rapidly changing over the past eight years that we have taught this course at MIT now over the past decade in fact even before we started teaching this course Ai and deep learning has really

    ....<skipping most of the transcript text>....
    
    idea but it's actually extremely easy to implement in practice because all you really have to do is just monitor the loss of over the course of training right and you just have to pick the model where the testing accuracy starts to get worse so I'll conclude this lecture by just summarizing three key points that we've cover covered in the class so far and this is a very g-pack class so the entire week is going to be like this and today is just the start so so far we've learned the fundamental building blocks of neural network starting all the way from just one neuron also called a perceptron we learned that we can stack these systems on top of each other to create a hierarchical network and how we can mathematically optimize those types of systems and then finally in the very very last part of the class we talked about just techniques tips and techniques for actually training and applying these systems into practice ice now in the next lecture we're going to hear from Ava on deep sequence modeling using rnns and also a really new and exciting algorithm and type of model called the Transformer which uh is built off of this principle of attention you're going to learn about it in the next class but let's for now just take a brief pause and let's resume in about five minutes just so we can switch speakers and Ava can start her presentation okay thank you",
    "url": "https://youtube.com/watch?v=ErnWZxJovaM",
    "thumbnails": {
      "default": {
        "url": "https://i.ytimg.com/vi/ErnWZxJovaM/default.jpg",
        "width": 120,
        "height": 90
      },
      "medium": {
        "url": "https://i.ytimg.com/vi/ErnWZxJovaM/mqdefault.jpg",
        "width": 320,
        "height": 180
      },
      "high": {
        "url": "https://i.ytimg.com/vi/ErnWZxJovaM/hqdefault.jpg",
        "width": 480,
        "height": 360
      },
      "standard": {
        "url": "https://i.ytimg.com/vi/ErnWZxJovaM/sddefault.jpg",
        "width": 640,
        "height": 480
      },
      "maxres": {
        "url": "https://i.ytimg.com/vi/ErnWZxJovaM/maxresdefault.jpg",
        "width": 1280,
        "height": 720
      }
    }
  },
  {
    "video_id": "SmZmBKc7Lrs",
    "title": "The Most Important Algorithm in Machine Learning",
    "description": "Shortform link: \nhttps://shortform.com/artem\n\nIn this video we will talk about backpropagation \u2013 an algorithm powering the entire field of machine learning and try to derive it from first principles.\n\nOUTLINE:\n00:00 Introduction\n01:28 Historical background\n02:50 Curve Fitting problem\n06:26 Random vs guided adjustments \n09:43 Derivatives\n14:34 Gradient Descent\n16:23 Higher dimensions\n21:36 Chain Rule Intuition\n27:01 Computational Graph and Autodiff\n36:24 Summary\n38:16 Shortform\n39:20 Outro\n\nUSEFUL RESOURCES:\nAndrej Karpathy's playlist: https://youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ&si=zBUZW5kufVPLVy9E\n\nJ\u00fcrgen Schmidhuber's blog on the history of backprop:\nhttps://people.idsia.ch/~juergen/who-invented-backpropagation.html\n\n\nCREDITS:\nIcons by https://www.freepik.com/",
    "published_at": "2024-04-01T03:23:54+00:00",
    "view_count": 566887,
    "comment_count": 543,
    "like_count": 25570,
    "favorite_count": 0,
    "channel_title": "Artem Kirsanov",
    "transcript": "what do nearly all machine Learning Systems have in common from GPT and M journey to Alpha fold and various models of the brain despite being designed to solve different problems having completely different architectures and being trained on different data there is something that unites all of them a single algorithm that runs under the hood of the training procedures in all of those cases this algorithm called back propagation is the foundation of the entire field of machine learning although its details are often 
    ....<skipping most of the transcript text>....
minimizing some sort of loss function does it calculate derivatives or could it be doing something totally different in the next video we are going to dive into the world of synaptic plasticity and talk about how biological neural networks learn in keeping with the topic of biological learning I'd like to take a moment to give a shout out to shortform a longtime partner of this channel short form is a platform which stay tuned for more interesting topics coming up goodbye and thank you for the interest in the [Music] brain for",
    "url": "https://youtube.com/watch?v=SmZmBKc7Lrs",
    "thumbnails": {
      "default": {
        "url": "https://i.ytimg.com/vi/SmZmBKc7Lrs/default.jpg",
        "width": 120,
        "height": 90
      },
      "medium": {
        "url": "https://i.ytimg.com/vi/SmZmBKc7Lrs/mqdefault.jpg",
        "width": 320,
        "height": 180
      },
      "high": {
        "url": "https://i.ytimg.com/vi/SmZmBKc7Lrs/hqdefault.jpg",
        "width": 480,
        "height": 360
      },
      "standard": {
        "url": "https://i.ytimg.com/vi/SmZmBKc7Lrs/sddefault.jpg",
        "width": 640,
        "height": 480
      },
      "maxres": {
        "url": "https://i.ytimg.com/vi/SmZmBKc7Lrs/maxresdefault.jpg",
        "width": 1280,
        "height": 720
      }
    }
  },
  {
    "video_id": "-zrY7P2dVC4",
    "title": "Physics Informed Neural Networks (PINNs) [Physics Informed Machine Learning]",
    "description": "This video introduces PINNs, or Physics Informed Neural Networks.  PINNs are a simple modification of a neural network that adds a PDE in the loss function to promote solutions that satisfy known physics.  For example, if we wish to model a fluid flow field and we know it is incompressible, we can add the divergence of the field in the loss function to drive it towards zero.  This approach relies on the automatic differentiability in neural networks (i.e., backpropagation) to compute partial derivatives used in the PDE loss function.  \n\nOriginal PINNs paper: https://www.sciencedirect.com/science/article/abs/pii/S0021999118307125\n\nPhysics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations\nM. Raissi  P. Perdikaris, G.E. Karniadakis\nJournal of Computational Physics\nVolume 378: 686-707, 2019\n\nThis video was produced at the University of Washington, and we acknowledge funding support from the Boeing Company\n\n%%% CHAPTERS %%%\n00:00 Intro\n01:54 PINNs: Central Concept\n06:38 Advantages and Disadvantages\n11:39 PINNs and Inference\n15:23 Recommended Resources\n19:33 Extending PINNs: Fractional PINNs\n21:40 Extending PINNs: Delta PINNs\n25:33 Failure Modes\n29:40 PINNs & Pareto Fronts\n31:57 Outro",
    "published_at": "2024-05-29T13:00:01+00:00",
    "view_count": 82929,
    "comment_count": 79,
    "like_count": 2285,
    "favorite_count": 0,
    "channel_title": "Steve Brunton",
    "transcript": "welcome back so in this video I'm going to introduce this idea of a physics informed neural network or a pin which was first presented in this paper by maer risey Paris paric Caris and George carneia dois and since its introduction it's become one of the Workhorse uh algorithms and kind of ideas in physics and form machine learning so it's based on a kind of uh neural network idea that 
    
    ....<skipping most of the transcript text>....

 machine learning people love it because it's easy for them physics people love it because it's easy you know to add neural networks into their you know physics uh kind of workflows and so it's really at that sweet spot um where it's kind of easy and pretty powerful okay um more on this definitely check out the resources in the description try to code it up yourself try to see where it does and doesn't work uh and we'll look at other methods soon all right thank you",
    "url": "https://youtube.com/watch?v=-zrY7P2dVC4",
    "thumbnails": {
      "default": {
        "url": "https://i.ytimg.com/vi/-zrY7P2dVC4/default.jpg",
        "width": 120,
        "height": 90
      },
      "medium": {
        "url": "https://i.ytimg.com/vi/-zrY7P2dVC4/mqdefault.jpg",
        "width": 320,
        "height": 180
      },
      "high": {
        "url": "https://i.ytimg.com/vi/-zrY7P2dVC4/hqdefault.jpg",
        "width": 480,
        "height": 360
      },
      "standard": {
        "url": "https://i.ytimg.com/vi/-zrY7P2dVC4/sddefault.jpg",
        "width": 640,
        "height": 480
      },
      "maxres": {
        "url": "https://i.ytimg.com/vi/-zrY7P2dVC4/maxresdefault.jpg",
        "width": 1280,
        "height": 720
      }
    }
  },
  {
    "video_id": "MD2fYip6QsQ",
    "title": "Who's Adam and What's He Optimizing? | Deep Dive into Optimizers for Machine Learning!",
    "description": "Welcome to our deep dive into the world of optimizers! In this video, we'll explore the crucial role that optimizers play in machine learning and deep learning. From Stochastic Gradient Descent to Adam, we cover the most popular algorithms, how they work, and when to use them. \n\n\ud83d\udd0d What You'll Learn:\n\nBasics of Optimization - Understand the fundamentals of how optimizers work to minimize loss functions\n\nGradient Descent Explained - Dive deep into the most foundational optimizer and its variants like SGD, Momentum, and Nesterov Accelerated Gradient\n\nAdvanced Optimizers - Get to grips with Adam, RMSprop, and AdaGrad, learning how they differ and their advantages\n\nIntuitive Math - Unveil the equations for each optimizer and learn how it stands out from the others\n\nReal World Benchmarks - See real world experiments from papers in domains ranging from computer vision to reinforcement learning to see how these optimizers fare against each other\n\n\ud83d\udd17 Extra Resources:\n\n3Blue1Brown - https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi\nArtem Kirsanov - https://www.youtube.com/watch?v=SmZmBKc7Lrs\n\n\ud83d\udccc Timestamps:\n0:00 - Introduction\n1:17 - Review of Gradient Descent\n5:37 - SGD w/ Momentum\n9:26 - Nesterov Accelerated Gradient\n10:55 - Root Mean Squared Propagation\n13:59 - Adaptive Gradients (AdaGrad)\n14:47 - Adam\n18:12 - Benchmarks\n22:01 - Final Thoughts\n\nStay tuned and happy learning!",
    "published_at": "2024-04-28T19:48:10+00:00",
    "view_count": 61915,
    "comment_count": 217,
    "like_count": 3080,
    "favorite_count": 0,
    "channel_title": "Sourish Kundu",
    "transcript": "hi everyone welcome back to the channel today we'll be talking about one of the most crucial components of the training process for machine learning models optimizers optimizers are the algorithms that determine how the weights of the machine learning model are tuned during back propagation it doesn't matter if we're talking about a neural network or something much simpler such as a linear regression model now you're probably already familiar with optimizers even if you didn't think so if you've heard of stochastic 

    ....<skipping most of the transcript text>....

usage across all the gpus along with minimizing communication between the gpus that's where libraries like Microsoft's deep speed with its zero redundancy optimizers comes in it cleverly splits up all the optimizer States across the gpus in such a way that training large l can experience a speed up of around 300% unfortunately diving into the deep speed library is out of the scope of today's video but I just wanted to share a quick example of why understanding optimizers is so crucial if all that sounds interesting to you let me know and I'd love to make a video about it however thank you guys for making it until the end and until next time bye-bye",
    "url": "https://youtube.com/watch?v=MD2fYip6QsQ",
    "thumbnails": {
      "default": {
        "url": "https://i.ytimg.com/vi/MD2fYip6QsQ/default.jpg",
        "width": 120,
        "height": 90
      },
      "medium": {
        "url": "https://i.ytimg.com/vi/MD2fYip6QsQ/mqdefault.jpg",
        "width": 320,
        "height": 180
      },
      "high": {
        "url": "https://i.ytimg.com/vi/MD2fYip6QsQ/hqdefault.jpg",
        "width": 480,
        "height": 360
      },
      "standard": {
        "url": "https://i.ytimg.com/vi/MD2fYip6QsQ/sddefault.jpg",
        "width": 640,
        "height": 480
      },
      "maxres": {
        "url": "https://i.ytimg.com/vi/MD2fYip6QsQ/maxresdefault.jpg",
        "width": 1280,
        "height": 720
      }
    }
  },
  {
    "video_id": "N9QY_fKXtFc",
    "title": "Neural Networks - the Simplest Explanation",
    "description": "Lately, AI has become extremely popular. At the core of the latest advancements in AI is Machine Learning. At the core of Machine Learning are Neural Networks, which we will explore in this video.\n\n\nChapters:\n00:00 Intro\n00:28 How do Neural Networks work?\n09:16 Training the Neural Network\n14:15 Backpropagation",
    "published_at": "2024-07-09T19:45:02+00:00",
    "view_count": 8622,
    "comment_count": 28,
    "like_count": 449,
    "favorite_count": 0,
    "channel_title": "Digital Genius",
    "transcript": "artificial intelligence is a broad concept for example algorithms used in chess engines pathf finding and even bots in video games can all be classified as AI however these algorithms typically follow a set of predefined rules a significant part of AI is machine learning which enables algorithms to learn and create their own rules at the core of machine learning are neural networks which we will explore in detail in this video in general neural networks are composed of neurons organized into layers the first layer is known as the input layer the final layer is the output layer and any layers in between are called hidden layers each neuron in a layer 
    ....<skipping most of the transcript text>....
    between four types of colored dots this network will have two inputs the X and Y positions of the dot and four outputs one for each color we'll see how the network learns this pattern [Music] finally let's challenge the network with a more complex pattern to see how well it can adapt and learn [Music]",
    "url": "https://youtube.com/watch?v=N9QY_fKXtFc",
    "thumbnails": {
      "default": {
        "url": "https://i.ytimg.com/vi/N9QY_fKXtFc/default.jpg",
        "width": 120,
        "height": 90
      },
      "medium": {
        "url": "https://i.ytimg.com/vi/N9QY_fKXtFc/mqdefault.jpg",
        "width": 320,
        "height": 180
      },
      "high": {
        "url": "https://i.ytimg.com/vi/N9QY_fKXtFc/hqdefault.jpg",
        "width": 480,
        "height": 360
      },
      "standard": {
        "url": "https://i.ytimg.com/vi/N9QY_fKXtFc/sddefault.jpg",
        "width": 640,
        "height": 480
      },
      "maxres": {
        "url": "https://i.ytimg.com/vi/N9QY_fKXtFc/maxresdefault.jpg",
        "width": 1280,
        "height": 720
      }
    }
  }
]
```

6. Agent saves the metadata and summary for each video as a JSON file.

Example end result:
```
[
    ...
    ...
]
```



## Installation

Install poetry with pipx

```bash
pipx install poetry
```

See [Installation Steps](https://python-poetry.org/docs/#installing-with-pipx)

## Adding packages

```bash
# create and activate a vitual env.
python -m venv venv
source venv/bin/activate (or use <venv>\Scripts\activate.bat for windows)

# in virtual environment, add packages from pyproject.toml
poetry install
```

## Configure Application
Copy example.env as .env file and add your keys.


## Run Application 
```bash
cd <project-root>
python ./app/workflows/ontology_creation_workflow.py 
```


## Dockerize Application
NOTE: Dockerfile is not fully tested yet.

This project folder includes a Dockerfile that allows you to easily build and host your LangServe app.

### Building the Image

To build the image, you simply:

```shell
docker build . -t youtube-agent-app
```

If you tag your image with something other than `youtube-agent-app`,
note it for use in the next step.


### Running the Image Locally

We also expose port 8080 with the `-p 8080:8080` option.

```shell
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8080:8080 youtube-agent-app
```

### Run tests
pytest --log-cli-level=DEBUG <test-file-or-dir>


