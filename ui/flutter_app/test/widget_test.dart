import 'package:flutter_test/flutter_test.dart';
import 'package:aegis_flutter_ui/main.dart';

void main() {
  testWidgets('HomePage has title', (WidgetTester tester) async {
    await tester.pumpWidget(const AegisApp());
    expect(find.text('Aegis IMX Dashboard'), findsOneWidget);
  });
}
