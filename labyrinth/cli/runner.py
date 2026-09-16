"""Main CLI runner for maze framework."""

import argparse
import sys
import importlib
import os
from pathlib import Path

from utils.maze_core.generator import MazeGenerator, TopologyType, CostMapType
from utils.maze_core.formats import MazeFormat
from utils.maze_core.simulator import Simulator
from utils.maze_core.agent import Agent


def discover_agents():
    """Discover available agents."""
    agents_dir = Path("agents")
    agents = {}

    if not agents_dir.exists():
        return agents

    for agent_folder in agents_dir.iterdir():
        if agent_folder.is_dir():
            agent_name = agent_folder.name
            agent_file = agent_folder / "agent.py"

            if agent_file.exists():
                try:
                    spec = importlib.util.spec_from_file_location(
                        agent_name, agent_file
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Find Agent subclass
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and
                            issubclass(attr, Agent) and
                            attr is not Agent):
                            agents[agent_name] = attr
                            break
                except Exception as e:
                    print(f"Error loading agent {agent_name}: {e}",
                          file=sys.stderr)

    return agents


def cmd_generate(args):
    """Generate maze command."""
    gen = MazeGenerator(args.width, args.height, seed=args.seed)

    topology = TopologyType(args.type)
    cost_map = CostMapType(args.cost_map)
    cost_range = tuple(map(int, args.cost_range.split(":")))

    maze = gen.generate(
        topology=topology,
        cost_map=cost_map,
        cost_range=cost_range,
    )

    MazeFormat.save(maze, args.output)
    print(f"\033[92mMaze generated: {args.output}\033[0m")


def cmd_run(args):
    """Run agent on maze command."""
    # Load or generate maze
    if args.maze_file:
        maze = MazeFormat.load(args.maze_file)
    else:
        gen = MazeGenerator(args.width, args.height, seed=args.seed)
        topology = TopologyType(args.type)
        cost_map = CostMapType(args.cost_map)
        cost_range = tuple(map(int, args.cost_range.split(":")))
        maze = gen.generate(
            topology=topology,
            cost_map=cost_map,
            cost_range=cost_range,
        )

    # Load agent
    agents = discover_agents()
    if args.agent not in agents:
        print(f"\033[91mAgent '{args.agent}' not found\033[0m",
              file=sys.stderr)
        sys.exit(1)

    agent_instance = agents[args.agent]()

    # Run simulation
    simulator = Simulator(maze, agent_instance, max_steps=args.max_steps,
                         visualize=args.visualize, speed=args.speed)
    result = simulator.run()

    # Print results
    print("\n" + "=" * 50)
    print(f"Agent: {result.agent_name}")
    print(f"Solved: {'YES' if result.solved else 'NO'}")
    print(f"Steps: {result.steps}")
    print(f"Path Cost: {result.path_cost:.1f}")
    print(f"Optimal Cost: {result.optimal_cost:.1f}")
    print(f"Optimality: {result.optimality_percentage:.1f}%")
    print(f"Nodes Explored: {result.nodes_explored}")
    print(f"Time: {result.execution_time_ms:.2f}ms")
    print(f"Invalid Moves: {result.invalid_moves}")
    print("=" * 50)

    if args.output_trace:
        import json
        with open(args.output_trace, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"Trace saved: {args.output_trace}")


def cmd_list(args):
    """List available agents/mazes."""
    if args.agents:
        agents = discover_agents()
        if agents:
            print("\033[92mAvailable agents:\033[0m")
            for name in sorted(agents.keys()):
                print(f"  - {name}")
        else:
            print("No agents found")

    if args.mazes:
        mazes_dir = Path("mazes/examples")
        if mazes_dir.exists():
            print("\033[92mExample mazes:\033[0m")
            for maze_file in sorted(mazes_dir.glob("*.maze")):
                print(f"  - {maze_file.name}")
        else:
            print("No mazes directory found")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Maze Search Algorithms Framework"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a maze")
    gen_parser.add_argument("--width", type=int, default=20)
    gen_parser.add_argument("--height", type=int, default=20)
    gen_parser.add_argument("--type", default="perfect",
                           choices=["perfect", "multiple", "unsolvable",
                                   "corridor", "open"])
    gen_parser.add_argument("--cost-map", default="uniform",
                           choices=["uniform", "random", "heatmap"])
    gen_parser.add_argument("--cost-range", default="1:1")
    gen_parser.add_argument("--seed", type=int, default=42)
    gen_parser.add_argument("--output", default="maze.maze")
    gen_parser.set_defaults(func=cmd_generate)

    # Run command
    run_parser = subparsers.add_parser("run", help="Run agent on maze")
    run_parser.add_argument("--agent", required=True)
    run_parser.add_argument("--maze-file", default=None)
    run_parser.add_argument("--width", type=int, default=20)
    run_parser.add_argument("--height", type=int, default=20)
    run_parser.add_argument("--type", default="perfect")
    run_parser.add_argument("--cost-map", default="uniform")
    run_parser.add_argument("--cost-range", default="1:1")
    run_parser.add_argument("--seed", type=int, default=42)
    run_parser.add_argument("--max-steps", type=int, default=10000)
    run_parser.add_argument("--output-trace", default=None)
    run_parser.add_argument("--visualize", action="store_true",
                           help="Show maze visualization in terminal")
    run_parser.add_argument("--speed", type=float, default=2.0,
                           help="Animation speed (higher = faster)")
    run_parser.set_defaults(func=cmd_run)

    # List command
    list_parser = subparsers.add_parser("list", help="List agents/mazes")
    list_parser.add_argument("--agents", action="store_true")
    list_parser.add_argument("--mazes", action="store_true")
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(0)

    try:
        args.func(args)
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
