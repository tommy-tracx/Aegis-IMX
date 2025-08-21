import 'package:flutter/material.dart';

void main() {
  runApp(const AegisApp());
}

/// Root widget for the Aegis IMX cross-platform application.
class AegisApp extends StatelessWidget {
  const AegisApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Aegis IMX',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

/// Home dashboard page with a responsive layout.
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Aegis IMX Dashboard')),
      body: Center(
        child: LayoutBuilder(
          builder: (context, constraints) {
            if (constraints.maxWidth >= 600) {
              // Tablet/Desktop layout
              return Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Expanded(child: InfoCard(title: 'Risk', value: '0.0')),
                  Expanded(child: InfoCard(title: 'PnL', value: '0.0')),
                  Expanded(child: InfoCard(title: 'Exposure', value: '0%')),
                ],
              );
            }
            // Mobile layout
            return ListView(
              padding: const EdgeInsets.all(16),
              children: const [
                InfoCard(title: 'Risk', value: '0.0'),
                InfoCard(title: 'PnL', value: '0.0'),
                InfoCard(title: 'Exposure', value: '0%'),
              ],
            );
          },
        ),
      ),
    );
  }
}

/// Card widget displaying a single metric.
class InfoCard extends StatelessWidget {
  final String title;
  final String value;

  const InfoCard({super.key, required this.title, required this.value});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 8),
            Text(value, style: Theme.of(context).textTheme.headlineMedium),
          ],
        ),
      ),
    );
  }
}
