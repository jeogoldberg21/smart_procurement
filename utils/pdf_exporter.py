"""
PDF Exporter for Purchase Orders
Generates professional PDF documents from PO data
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import os


class PDFExporter:
    """
    Export purchase orders to PDF format
    """
    
    def __init__(self, output_dir='data/purchase_orders/pdf'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#667eea'),
            borderPadding=5,
            backColor=colors.HexColor('#f8f9fa')
        ))
        
        # Info style
        self.styles.add(ParagraphStyle(
            name='InfoText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#4a5568'),
            spaceAfter=6
        ))
        
        # Highlight style
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#10b981'),
            fontName='Helvetica-Bold'
        ))
    
    def export_po_to_pdf(self, po_data: dict, filename: str = None) -> str:
        """
        Export PO to PDF
        
        Args:
            po_data: Purchase order dictionary
            filename: Optional custom filename
        
        Returns:
            Path to generated PDF file
        """
        if filename is None:
            filename = f"{po_data['po_number']}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        
        # Header
        story.extend(self._build_header(po_data))
        story.append(Spacer(1, 0.3*inch))
        
        # PO Info
        story.extend(self._build_po_info(po_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Vendor Info
        story.extend(self._build_vendor_section(po_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Material Details
        story.extend(self._build_material_section(po_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Financial Summary
        story.extend(self._build_financial_section(po_data))
        story.append(Spacer(1, 0.2*inch))
        
        # AI Recommendation
        story.extend(self._build_ai_section(po_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Delivery Info
        story.extend(self._build_delivery_section(po_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Terms
        story.extend(self._build_terms_section(po_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Approvals
        story.extend(self._build_approvals_section(po_data))
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        story.extend(self._build_footer(po_data))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _build_header(self, po_data: dict) -> list:
        """Build PDF header"""
        elements = []
        
        # Title
        title = Paragraph("PURCHASE ORDER", self.styles['CustomTitle'])
        elements.append(title)
        
        # Company info (you can customize this)
        company_info = Paragraph(
            "<b>Smart Procurement System</b><br/>"
            "AI-Powered Material Procurement<br/>"
            "Email: procurement@company.com | Phone: +91-XXXXXXXXXX",
            self.styles['InfoText']
        )
        elements.append(company_info)
        
        return elements
    
    def _build_po_info(self, po_data: dict) -> list:
        """Build PO information section"""
        elements = []
        
        # Create table with PO details
        data = [
            ['PO Number:', po_data['po_number'], 'Date:', po_data['created_date']],
            ['Status:', po_data['status'], 'Created By:', po_data['created_by']]
        ]
        
        table = Table(data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(table)
        return elements
    
    def _build_vendor_section(self, po_data: dict) -> list:
        """Build vendor information section"""
        elements = []
        
        header = Paragraph("VENDOR INFORMATION", self.styles['SectionHeader'])
        elements.append(header)
        
        vendor = po_data['vendor']
        data = [
            ['Vendor Name:', vendor['name']],
            ['Rating:', f"{vendor['rating']}/5.0"],
            ['Payment Terms:', vendor['payment_terms']],
            ['Reliability:', vendor['reliability']]
        ]
        
        table = Table(data, colWidths=[2*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(table)
        return elements
    
    def _build_material_section(self, po_data: dict) -> list:
        """Build material details section"""
        elements = []
        
        header = Paragraph("MATERIAL DETAILS", self.styles['SectionHeader'])
        elements.append(header)
        
        material = po_data['material']
        data = [
            ['Material:', material['name']],
            ['Quantity:', f"{material['quantity']} {material['unit']}"],
            ['Unit Price:', f"${material['unit_price']:.2f}/{material['unit']}"],
            ['Market Price:', f"${material['current_market_price']:.2f}/{material['unit']}"]
        ]
        
        table = Table(data, colWidths=[2*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(table)
        return elements
    
    def _build_financial_section(self, po_data: dict) -> list:
        """Build financial summary section"""
        elements = []
        
        header = Paragraph("FINANCIAL SUMMARY", self.styles['SectionHeader'])
        elements.append(header)
        
        financial = po_data['financial']
        data = [
            ['Subtotal:', f"${financial['subtotal']:,.2f}"],
            ['Tax ({:.0f}%):'.format(financial['tax_rate']*100), f"${financial['tax_amount']:,.2f}"],
            ['Total Amount:', f"${financial['total_amount']:,.2f}"],
            ['Potential Savings:', f"${financial['potential_savings']:,.2f}"]
        ]
        
        table = Table(data, colWidths=[2*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('BACKGROUND', (0, 2), (1, 2), colors.HexColor('#667eea')),
            ('BACKGROUND', (0, 3), (1, 3), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 1), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 2), (1, 2), colors.white),
            ('TEXTCOLOR', (0, 3), (1, 3), colors.white),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (0, 2), (1, 3), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTSIZE', (0, 2), (1, 2), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(table)
        return elements
    
    def _build_ai_section(self, po_data: dict) -> list:
        """Build AI recommendation section"""
        elements = []
        
        header = Paragraph("AI RECOMMENDATION CONTEXT", self.styles['SectionHeader'])
        elements.append(header)
        
        ai = po_data['ai_recommendation']
        data = [
            ['Recommendation:', ai['recommendation']],
            ['Reason:', ai['reason']],
            ['Confidence:', ai['confidence']],
            ['Forecast Change:', ai['forecast_change']]
        ]
        
        table = Table(data, colWidths=[2*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(table)
        return elements
    
    def _build_delivery_section(self, po_data: dict) -> list:
        """Build delivery information section"""
        elements = []
        
        header = Paragraph("DELIVERY INFORMATION", self.styles['SectionHeader'])
        elements.append(header)
        
        delivery = po_data['delivery']
        data = [
            ['Expected Delivery:', delivery['expected_date']],
            ['Delivery Time:', f"{delivery['delivery_days']} days"],
            ['Delivery Address:', delivery['delivery_address']],
            ['Contact Person:', delivery['contact_person']]
        ]
        
        table = Table(data, colWidths=[2*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(table)
        return elements
    
    def _build_terms_section(self, po_data: dict) -> list:
        """Build terms and conditions section"""
        elements = []
        
        header = Paragraph("TERMS AND CONDITIONS", self.styles['SectionHeader'])
        elements.append(header)
        
        terms_text = "<br/>".join([f"{i+1}. {term}" for i, term in enumerate(po_data['terms'])])
        terms = Paragraph(terms_text, self.styles['InfoText'])
        elements.append(terms)
        
        return elements
    
    def _build_approvals_section(self, po_data: dict) -> list:
        """Build approvals section"""
        elements = []
        
        header = Paragraph("APPROVAL STATUS", self.styles['SectionHeader'])
        elements.append(header)
        
        approvals = po_data['approvals']
        data = [
            ['Role', 'Name', 'Status', 'Date'],
            ['Requester', approvals['requester']['name'], approvals['requester']['status'], 
             approvals['requester']['date'] or 'N/A'],
            ['Manager', approvals['manager']['name'], approvals['manager']['status'], 
             approvals['manager']['date'] or 'N/A'],
            ['Finance', approvals['finance']['name'], approvals['finance']['status'], 
             approvals['finance']['date'] or 'N/A']
        ]
        
        table = Table(data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(table)
        return elements
    
    def _build_footer(self, po_data: dict) -> list:
        """Build PDF footer"""
        elements = []
        
        footer_text = (
            f"<i>This is a computer-generated document. No signature is required.</i><br/>"
            f"Generated by Smart Procurement System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        footer = Paragraph(footer_text, self.styles['InfoText'])
        elements.append(footer)
        
        return elements


# Global instance
_pdf_exporter = None

def get_pdf_exporter():
    """Get or create global PDF exporter instance"""
    global _pdf_exporter
    if _pdf_exporter is None:
        _pdf_exporter = PDFExporter()
    return _pdf_exporter


if __name__ == '__main__':
    # Test PDF export
    import json
    
    # Sample PO data
    sample_po = {
        'po_number': 'PO-202510-1001',
        'status': 'DRAFT',
        'created_date': '2025-10-16 11:30:00',
        'created_by': 'Procurement Manager',
        'material': {
            'name': 'Copper',
            'quantity': 100,
            'unit': 'tons',
            'unit_price': 8450.00,
            'current_market_price': 8500.00
        },
        'vendor': {
            'name': 'Global Metals Inc.',
            'rating': 4.5,
            'payment_terms': 'Net 30',
            'reliability': 'High'
        },
        'delivery': {
            'expected_date': '2025-10-23',
            'delivery_days': 7,
            'delivery_address': 'Warehouse A',
            'contact_person': 'Procurement Manager'
        },
        'financial': {
            'subtotal': 845000.00,
            'tax_rate': 0.18,
            'tax_amount': 152100.00,
            'total_amount': 997100.00,
            'potential_savings': 5000.00
        },
        'ai_recommendation': {
            'recommendation': 'BUY NOW',
            'reason': 'Price expected to rise by 2.5%',
            'confidence': 'High',
            'forecast_change': '+2.50%'
        },
        'inventory_context': {
            'current_stock': 150,
            'min_threshold': 100,
            'daily_consumption': 15,
            'days_remaining': 10.0
        },
        'terms': [
            "Payment terms as per vendor agreement",
            "Quality inspection upon delivery",
            "Penalties for late delivery as per contract",
            "Material specifications as per industry standards",
            "Insurance coverage during transit"
        ],
        'approvals': {
            'requester': {'name': 'Procurement Manager', 'status': 'APPROVED', 'date': '2025-10-16'},
            'manager': {'name': 'Pending', 'status': 'PENDING', 'date': None},
            'finance': {'name': 'Pending', 'status': 'PENDING', 'date': None}
        }
    }
    
    exporter = PDFExporter()
    pdf_path = exporter.export_po_to_pdf(sample_po)
    print(f"✓ PDF generated: {pdf_path}")
